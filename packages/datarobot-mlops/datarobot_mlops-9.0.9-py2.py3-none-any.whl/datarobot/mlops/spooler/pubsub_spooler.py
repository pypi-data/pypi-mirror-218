from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import sys
import time
from builtins import dict
from builtins import super

import datarobot.mlops.install_aliases  # noqa: F401
from datarobot.mlops.channel.record import Record
from datarobot.mlops.common import config
from datarobot.mlops.common.config import ConfigConstants
from datarobot.mlops.common.enums import MLOpsSpoolAction
from datarobot.mlops.common.enums import SpoolerType
from datarobot.mlops.common.exception import DRSpoolerException
from datarobot.mlops.spooler.record_spooler import RecordSpooler
from google.api_core.exceptions import AlreadyExists
from google.cloud import pubsub_v1

#  Copyright (c) 2020 DataRobot, Inc. and its affiliates. All rights reserved.
#  Last updated 2023.
#
#  DataRobot, Inc. Confidential.
#  This is unpublished proprietary source code of DataRobot, Inc. and its affiliates.
#  The copyright notice above does not evidence any actual or intended publication of
#  such source code.
#
#  This file and its contents are subject to DataRobot Tool and Utility Agreement.
#  For details, see
#  https://www.datarobot.com/wp-content/uploads/2021/07/DataRobot-Tool-and-Utility-Agreement.pdf.


logger = logging.getLogger(__name__)
futures = dict()
published_messages = 0


class PubSubRecordSpooler(RecordSpooler):
    # PubSub has max 10MB message size limit
    # Note: the limit is 10,000,000 not 10 * 1024 * 1024
    PUBSUB_MESSAGE_SIZE_LIMIT_IN_BYTE = 1000 * 1000 * 10

    # Note that dequeue is only used by tests
    PUBSUB_DEFAULT_MAX_RECORDS_TO_DEQUEUE = 10
    PUBSUB_DEFAULT_ACK_DEADLINE_SECONDS = 600  # 10 minutes

    PUBSUB_DEFAULT_SLEEP_TIME = 1
    PUBSUB_DEFAULT_MAX_PENDING_MESSAGES = 10
    PUBSUB_DEFAULT_MAX_WAIT_FOR_PENDING_MESSAGES_SECONDS = 180  # 3 minutes

    def __init__(self):
        super(PubSubRecordSpooler, self).__init__()
        self.initialized = False

        self._project_id = None
        self._topic_name = None
        self._max_flush_time = None
        self._subscription_name = None

        self._full_topic_name = None
        self._publisher = None
        self._dequeue_enabled = False
        self._subscriber = None
        self._full_subscription_name = None

        self._last_connect_time = 0
        self._ack_deadline = 0
        self._max_records_dequeue = 0

        self._max_wait_time_for_pending_msgs = 0
        self._max_pending_messages = 0
        if sys.version_info < (3, 0):
            self._logger.error("PubSub only supports Python3.")
            raise Exception("PubSub only supports Python 3.")

    @staticmethod
    def get_type():
        return SpoolerType.PUBSUB

    def get_required_config(self):
        return [ConfigConstants.PUBSUB_PROJECT_ID, ConfigConstants.PUBSUB_TOPIC_NAME]

    def get_optional_config(self):
        return [ConfigConstants.PUBSUB_MAX_FLUSH_SECONDS, ConfigConstants.PUBSUB_SUBSCRIPTION_NAME]

    def set_config(self):
        missing = super(PubSubRecordSpooler, self).get_missing_config()
        if len(missing) > 0:
            raise DRSpoolerException("Configuration values missing: {}".format(missing))

        data_format_str = config.get_config_default(
            ConfigConstants.SPOOLER_DATA_FORMAT, self.JSON_DATA_FORMAT_STR
        )
        if data_format_str != self.JSON_DATA_FORMAT_STR:
            raise DRSpoolerException(
                "Data Format: '{}' is not support for the PubSub Spooler".format(data_format_str)
            )

        self._max_wait_time_for_pending_msgs = config.get_config_default(
            ConfigConstants.PUBSUB_MAX_WAIT_FOR_PENDING_MESSAGES_SECONDS,
            self.PUBSUB_DEFAULT_MAX_WAIT_FOR_PENDING_MESSAGES_SECONDS,
        )
        self._max_pending_messages = config.get_config_default(
            ConfigConstants.PUBSUB_MAX_PENDING_MESSAGES, self.PUBSUB_DEFAULT_MAX_PENDING_MESSAGES
        )

        self._ack_deadline = config.get_config_default(
            ConfigConstants.PUBSUB_ACK_DEADLINE_SECONDS, self.PUBSUB_DEFAULT_ACK_DEADLINE_SECONDS
        )
        self._project_id = config.get_config(ConfigConstants.PUBSUB_PROJECT_ID)
        self._topic_name = config.get_config(ConfigConstants.PUBSUB_TOPIC_NAME)
        self._max_flush_time = config.get_config_default(
            ConfigConstants.PUBSUB_MAX_FLUSH_SECONDS, -1
        )

        self._max_records_dequeue = config.get_config_default(
            ConfigConstants.SPOOLER_DEQUEUE_MAX_RECORDS_PER_CALL,
            self.PUBSUB_DEFAULT_MAX_RECORDS_TO_DEQUEUE,
        )
        # NOTE: subscription_name is only used for testing
        self._subscription_name = config.get_config_default(
            ConfigConstants.PUBSUB_SUBSCRIPTION_NAME, None
        )

        self._full_topic_name = "projects/{project_id}/topics/{topic}".format(
            project_id=self._project_id, topic=self._topic_name
        )

        # dequeue/subscribe is only needed for testing
        if self._subscription_name is not None:
            self._dequeue_enabled = True

            self._full_subscription_name = "projects/{project_id}/subscriptions/{sub}".format(
                project_id=self._project_id, sub=self._subscription_name
            )
            self._logger.info(
                "PubSub full subscription name is {}".format(self._full_subscription_name)
            )
        else:
            self._logger.info("No subscription name provided. Dequeue will not be supported.")

    def open(self, action=MLOpsSpoolAction.ENQUEUE):
        self.set_config()

        # create publisher
        self._publisher = pubsub_v1.PublisherClient()

        if self._subscription_name is not None:
            self._subscriber = pubsub_v1.SubscriberClient()

        try:
            self._logger.info("Creating topic {}...".format(self._topic_name))
            self._publisher.create_topic(self._full_topic_name)
            self._logger.info("Created topic {}...".format(self._topic_name))

        except AlreadyExists:
            self._logger.info("Topic {} already exists.".format(self._topic_name))

        # dequeue/subscribe is only needed for testing
        if self._dequeue_enabled:
            self._subscriber = pubsub_v1.SubscriberClient()
            self._logger.info("Creating subscription {}...".format(self._full_subscription_name))
            try:
                self._subscriber.create_subscription(
                    name=self._full_subscription_name, topic=self._full_topic_name
                )
                self._logger.info("Subscription {} created".format(self._full_subscription_name))

            except AlreadyExists:
                self._logger.info(
                    "Subscription {} already exists.".format(self._full_subscription_name)
                )

        self.initialized = True

    # used only for testing
    def delete_subscription(self):
        self._subscriber.delete_subscription(self._full_subscription_name)

    # used only for testing
    def delete_topic(self):
        self._publisher.delete_topic(self._full_topic_name)

    # Used by mlops-cli for dequeue
    def empty(self):
        return self._empty_count >= self.DEFAULT_CONSUMER_MAX_FETCH_BEFORE_SET_EMPTY

    def ack_records(self, records_id_list):
        if not self.enable_dequeue_ack_record:
            return

        ack_ids = [
            self._records_pending_ack[record_id]
            for record_id in records_id_list
            if record_id in self._records_pending_ack
        ]
        if len(ack_ids) > 0:
            self._subscriber.acknowledge(self._full_subscription_name, ack_ids)

    def close(self):
        flush_time_spent = 0
        wait_interval = 5
        while futures:
            self._logger.info("Waiting for {} unacked messages.".format(len(futures)))
            time.sleep(wait_interval)
            flush_time_spent += wait_interval
            if 0 < self._max_flush_time < wait_interval:
                break

    def get_message_byte_size_limit(self):
        return self.PUBSUB_MESSAGE_SIZE_LIMIT_IN_BYTE

    def publish_single_record(self, record):
        if not self.initialized:
            raise DRSpoolerException("Spooler must be opened before using.")

        if not isinstance(record, Record):
            raise DRSpoolerException("Argument of type {} is expected", type(Record))

        record_json = record.to_json()
        record_bytearray = record_json.encode("utf-8")
        record_size = len(record_bytearray)

        # Check size limit
        if record_size > self.get_message_byte_size_limit():
            self._logger.info("Cannot enqueue record of size: {}".format(record_size))
            raise DRSpoolerException(
                "Record size {} over maximum {}.".format(
                    record_size, self.get_message_byte_size_limit()
                )
            )
        t0 = time.time()
        while time.time() < t0 + self._max_wait_time_for_pending_msgs:
            if len(futures) < self._max_pending_messages:
                futures.update({record_json: None})
                f = self._publisher.publish(self._full_topic_name, record_bytearray)
                futures[record_json] = f
                f.add_done_callback(_get_callback(f, record_json))
                return
            else:
                time.sleep(self.PUBSUB_DEFAULT_SLEEP_TIME)
        else:
            raise DRSpoolerException(
                "Unable to send record to spooler because there are too many records in progress. "
                "You may need to increase MLOPS_PUBSUB_MAX_PENDING_MESSAGE (current value is 10) "
                "or MLOPS_PUBSUB_MAX_WAIT_FOR_PENDING_MESSAGES_SECONDS (current value is 180 sec.)"
            )

    def enqueue(self, record_list):
        if not self.initialized:
            raise DRSpoolerException("Spooler must be opened before using.")

        self._logger.debug("Publishing {} records".format(len(record_list)))

        if len(record_list) < 1:
            return

        for record in record_list:
            self.publish_single_record(record)

        self._logger.debug("Published {} messages".format(len(record_list)))

    # dequeue is only provided for testing
    def dequeue(self):
        if self._dequeue_enabled is False:
            raise DRSpoolerException(
                " You must provide a subscription name on spooler creation to \
            enable dequeue."
            )

        if not self.initialized:
            raise DRSpoolerException("Spooler must be opened before using.")

        record_list = []
        response = self._subscriber.pull(
            self._full_subscription_name, max_messages=self._max_records_dequeue
        )
        ack_ids = []
        for msg in response.received_messages:
            try:
                msg_bytes = msg.message.data
                message_json = msg_bytes.decode("utf-8")
                record = Record.from_json(message_json)
                self._logger.debug(
                    "Received message for deployment {}".format(record.get_deployment_id())
                )
                record_list.append(record)

                self._add_pending_record(record.get_id(), msg.ack_id)
                ack_ids.append(msg.ack_id)
            except Exception as e:
                self._logger.error("Unable to dequeue message: {}".format(e))

        self._logger.debug("Received {} messages.".format(len(ack_ids)))
        if len(ack_ids) > 0:
            if self.enable_dequeue_ack_record:
                self._subscriber.modify_ack_deadline(
                    subscription=self._full_subscription_name,
                    ack_ids=ack_ids,
                    ack_deadline_seconds=self._ack_deadline,
                )
            else:
                self._subscriber.acknowledge(self._full_subscription_name, ack_ids)

        self._update_empty_count(len(record_list))

        return record_list

    def __dict__(self):
        return {
            ConfigConstants.SPOOLER_TYPE.name: SpoolerType.PUBSUB.name,
            ConfigConstants.PUBSUB_PROJECT_ID.name: self._project_id,
            ConfigConstants.PUBSUB_TOPIC_NAME.name: self._topic_name,
            ConfigConstants.PUBSUB_MAX_FLUSH_SECONDS.name: self._max_flush_time,
            ConfigConstants.PUBSUB_SUBSCRIPTION_NAME.name: self._subscription_name,
        }


def _get_callback(future, data):
    def callback(f):
        try:
            futures.pop(data)
        except Exception:
            logger.error("Received exception {} for {}.".format(f.exception(), data))

    return callback
