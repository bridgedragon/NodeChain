#!/usr/bin/python3
from logger import logger
from rpcutils import rpcutils, errorhandler as rpcerrorhandler
from wsutils import wsutils, topics
from wsutils.broker import Broker
from .constants import *
from . import utils


@wsutils.webSocketMethod
def subscribeAddressBalance(subscriber, id, params):

    logger.printInfo(f"Executing WS method subscribeAddressBalance with id {id} and params {params}")

    requestSchema = utils.getWSRequestMethodSchema(SUBSCRIBE_ADDRESS_BALANCE)

    err = rpcutils.validateJSONRPCSchema(params, requestSchema)
    if err is not None:
        raise rpcerrorhandler.BadRequestError(err.message)

    return subscriber.subscribeToTopic(Broker(), topics.Topic(topics.ADDRESS_BALANCE_TOPIC + topics.TOPIC_SEPARATOR + params[ADDRESS], utils.closingAddrBalanceTopic))


@wsutils.webSocketMethod
def unsubscribeAddressBalance(subscriber, id, params):

    logger.printInfo(f"Executing WS method unsubscribeAddressBalance with id {id} and params {params}")

    requestSchema = utils.getWSRequestMethodSchema(UNSUBSCRIBE_ADDRESS_BALANCE)

    err = rpcutils.validateJSONRPCSchema(params, requestSchema)
    if err is not None:
        raise rpcerrorhandler.BadRequestError(err.message)

    return subscriber.unsubscribeFromTopic(Broker(), topics.ADDRESS_BALANCE_TOPIC + topics.TOPIC_SEPARATOR + params[ADDRESS])


@wsutils.webSocketMethod
def subscribeToNewBlocks(subscriber, id, params):

    logger.printInfo(f"Executing WS method subscribeToNewBlock with id {id} and params {params}")

    requestSchema = utils.getWSRequestMethodSchema(SUBSCRIBE_TO_NEW_BLOCKS)

    err = rpcutils.validateJSONRPCSchema(params, requestSchema)
    if err is not None:
        raise rpcerrorhandler.BadRequestError(err.message)

    return subscriber.subscribeToTopic(Broker(), topics.Topic(topics.NEW_BLOCKS_TOPIC, None))


@wsutils.webSocketMethod
def unsubscribeFromNewBlocks(subscriber, id, params):

    logger.printInfo(f"Executing WS method unsubscribeToNewBlockMine with id {id} and params {params}")

    requestSchema = utils.getWSRequestMethodSchema(UNSUBSCRIBE_FROM_NEW_BLOCKS)

    err = rpcutils.validateJSONRPCSchema(params, requestSchema)
    if err is not None:
        raise rpcerrorhandler.BadRequestError(err.message)

    return subscriber.unsubscribeFromTopic(Broker(), topics.NEW_BLOCKS_TOPIC)
