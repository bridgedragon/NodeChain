#!/usr/bin/python3
import threading
from logger import logger
from .singleton import Singleton
from .subscribers import SubscriberInterface
from .constants import *


class Broker(object, metaclass=Singleton):

    def __init__(self):

        self.topicSubscriptions = {}  # Topic -> {"Subs":[Sub1, Sub2], "ClosingFunc":func}

    def attach(self, subscriber, topic):

        logger.printInfo(f"Attaching subscriber {subscriber.subscriberID} to topic [{topic.name}]")

        if not issubclass(type(subscriber), SubscriberInterface):
            logger.printWarning("Trying to attach unknown subscriber class")
            return {
                SUBSCRIBED: False
            }

        if topic.name not in self.topicSubscriptions:
            self.topicSubscriptions[topic.name] = {
                SUBSCRIBERS: [],
                CLOSING_TOPIC_FUNC: topic.closingHandler
            }

        if subscriber not in self.topicSubscriptions[topic.name][SUBSCRIBERS]:
            logger.printInfo(f"Subscriber {subscriber.subscriberID} atached successfully to topic [{topic.name}]")
            self.topicSubscriptions[topic.name][SUBSCRIBERS].append(subscriber)
            return {
                SUBSCRIBED: True
            }
        else:
            logger.printInfo(f"Subscriber {subscriber.subscriberID} already atached to topic [{topic.name}]")
            return {
                SUBSCRIBED: False
            }

    def detach(self, subscriber, topicName=""):

        logger.printInfo(f"Detaching subscriber {subscriber.subscriberID} from topic [{topicName}]")

        if not issubclass(type(subscriber), SubscriberInterface):
            logger.printWarning("Trying to detach unknown subscriber class")
            return {
                UNSUBSCRIBED: False
            }

        if topicName not in self.topicSubscriptions:
            logger.printWarning(f"Trying to detach subscriber {subscriber.subscriberID} from unknown topic [{topicName}]")
            return {
                UNSUBSCRIBED: False
            }
        elif subscriber in self.topicSubscriptions[topicName][SUBSCRIBERS]:
            self.topicSubscriptions[topicName][SUBSCRIBERS].remove(subscriber)
            logger.printInfo(f"Subscriber {subscriber.subscriberID} detached from topic [{topicName}]")

            if len(self.topicSubscriptions[topicName][SUBSCRIBERS]) == 0:
                logger.printWarning(f"No more subscribers for topic [{topicName}]")
                del self.topicSubscriptions[topicName]

            return {
                UNSUBSCRIBED: True
            }
        else:
            logger.printWarning(f"Subscriber {subscriber.subscriberID} can not be detached because it is not subscribed to topic [{topicName}]")
            return {
                UNSUBSCRIBED: False
            }

    def route(self, topicName="", message=""):

        logger.printInfo(f"Routing message of topic [{topicName}]: {message}")

        if topicName in self.topicSubscriptions:

            for subscriber in self.topicSubscriptions[topicName][SUBSCRIBERS]:

                subscriberNotificationThread = threading.Thread(target=_notifySubscriber, args=(subscriber, topicName, message), daemon=True)
                subscriberNotificationThread.start()

    def removeSubscriber(self, subscriber):

        logger.printInfo(f"Removing subscriber {subscriber.subscriberID} from subsbribed topics")

        if not issubclass(type(subscriber), SubscriberInterface):
            logger.printWarning("Trying to remove unknown subscriber class")
            return False

        for topicName in subscriber.topicsSubscribed:
            topicClosingFunc = self.topicSubscriptions[topicName][CLOSING_TOPIC_FUNC]
            self.detach(subscriber, topicName)

            if not self.topicHasSubscribers(topicName):
                logger.printInfo(f"Calling closing func to topic [{topicName}]")
                topicClosingFunc(topicName)

    def isTopic(self, topicName):
        return topicName in self.topicSubscriptions

    def getSubTopics(self, topicName):
        return [topicSubscription[len(topicName) + 1:] for topicSubscription in self.topicSubscriptions if topicName in topicSubscription]

    def topicHasSubscribers(self, topicName):
        if topicName in self.topicSubscriptions:
            return len(self.topicSubscriptions[topicName][SUBSCRIBERS]) != 0
        return False

    def getTopicSubscribers(self, topicName):

        if topicName in self.topicSubscriptions:
            return self.topicSubscriptions[topicName][SUBSCRIBERS]
        return []

    def getTopicNameSubscriptions(self):
        return list(self.topicSubscriptions.keys())


def _notifySubscriber(subscriber, topicName, message):
    subscriber.onMessage(topicName, message)
