#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from typing import Dict, Callable
import logging
import logging.config
import importlib
from uuid import uuid4
from firebird.rabbitmq import get_connection, RabbitMQ
from firebird import zkdb
import tempfile
import os
import jinja2
from libs import render_template
from kubernetes import client,config as k8_config,utils

logger = logging.getLogger(__name__)

def register_command(config:dict, pipeline_namespace_name:str, pipeline_image_name:str, pipeline_module_name:str):
    pipeline = importlib.import_module(pipeline_module_name).get_pipeline(None)
    pipeline_info = pipeline.to_json()

    mq = RabbitMQ(
        connection = get_connection(**config["rabbitmq"]),
        topic = pipeline.id
    )
    # create rabbitmq topic, etc
    mq.initialize()

    with zkdb(**config['zookeeper']) as db:
        db.register_pipeline(pipeline.id, pipeline_namespace_name, pipeline_image_name, pipeline_module_name, pipeline_info)

def unregister_command(config:dict, pipeline_id:str):
    with zkdb(**config['zookeeper']) as db:
        db.unregister_pipeline(pipeline_id)

def list_command(config):
    with zkdb(**config['zookeeper']) as db:
        pipelines = db.get_pipelines()

    for pipeline in pipelines:
        print(f"{pipeline['info']['id']}:")
        print(f"    namespace: {pipeline['namespace_name']}")
        print(f"    image:     {pipeline['image_name']}")
        print(f"    module   : {pipeline['module']}")
        if len(pipeline["executors"]) == 0:
            print("    executors: None")
        else:
            print("    executors:")
            for executor in pipeline["executors"]:
                executor_info = executor["info"]
                print(f"        {executor_info['id']}:")
                print(f"            start_time            = {executor_info['start_time']}")
                print(f"            pid                   = {executor_info['pid']}")
                print(f"            generator_id          = {executor_info['generator_id']}")

def stop_command(config:dict, pipeline_id:str):
    with zkdb(**config['zookeeper']) as db:
        pipeline = db.get_pipeline(pipeline_id)

    k8_config.load_kube_config()
    api = client.AppsV1Api()
    
    resp = api.delete_namespaced_deployment(
        name=pipeline_id,
        namespace=pipeline["namespace_name"],
        pretty=True,
        body=client.V1DeleteOptions(
            propagation_policy="Foreground", grace_period_seconds=300
        ),
    )
    print(resp)
    resp = api.delete_namespaced_stateful_set(
        name=f"{pipeline_id}-g",
        namespace=pipeline["namespace_name"],
        pretty=True,
        body=client.V1DeleteOptions(
            propagation_policy="Foreground", grace_period_seconds=300
        ),
    )
    print(resp)


def start_command(config, pipeline_id, replicas):
    to_apply = ""
    with zkdb(**config['zookeeper']) as db:
        pipeline = db.get_pipeline(pipeline_id)

        generator_ids = []
        for node in pipeline["nodes"]:
            input_port_count = 0
            for port in node["ports"]:
              if port["type"] == "INPUT": # hack, better use PortType enum
                input_port_count += 1
            if input_port_count == 0:
                generator_ids.append(node["id"])

        to_apply = render_template("pipeline.yaml", {
            "pipeline_namespace_name": pipeline["namespace_name"],
            "pipeline_image_name": pipeline["image_name"],
            "pipeline_id": pipeline_id,
            "replicas": replicas,
            "generator_ids": generator_ids
        })

    k8_config.load_kube_config()
    k8s_client = client.ApiClient()
    with tempfile.NamedTemporaryFile(mode='wt', delete=False) as tf:
        tf.write(to_apply)
    try:
        print("Use following deployment:")
        print(os.linesep)
        print(os.linesep)
        print(to_apply)
        print(os.linesep)
        print(os.linesep)
        utils.create_from_yaml(k8s_client, tf.name, verbose=True)
    finally:
        os.remove(tf.name)
