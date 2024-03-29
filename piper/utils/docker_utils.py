from piper.configurations import get_configuration

import sys
import time

import docker
# from loguru import logger
from piper.utils.logger_utils import logger

cfg = get_configuration()


def get_image(docker_client, image_name):
    try:
        cur_image = docker_client.images.get(image_name)
        return cur_image
    except docker.errors.ImageNotFound:
        logger.info(f'image with tag {image_name} not found')
        return False


def delete_image(docker_client, image_tag):
    try:
        docker_client.images.remove(image_tag, force=True)
        return True
    except Exception as e:
        logger.error('error while remove image', e)
        return False


def get_container(docker_client, container_name):
    try:
        cur_container = docker_client.containers.get(container_name)
        return cur_container
    except docker.errors.NotFound:
        logger.info(f'container with name {container_name} not found')
        return False
    except Exception as e:
        logger.error(f'non defined exeption {e}')
        return False


def get_container_with_status(docker_client, container_name):
    try:
        cur_container = docker_client.containers.get(container_name)
        if cur_container:
                status = cur_container.status
                cont_id = cur_container.id
                return cur_container, status, cont_id
    except docker.errors.NotFound:
        logger.info(f'container with name {container_name} not found')
        return False
    except Exception as e:
        logger.error(f'non defined exeption {e}')
        return False        


def stop_container(docker_client, container_name):
    try:
        cur_container = docker_client.containers.get(container_name)
        cur_container.stop()
        return True
    except docker.errors.NotFound:
        logger.error(f'container for stop with name {container_name} not found')
        return False
    except docker.errors.APIError:
        logger.error(f'error while stop container {container_name}')
        return False


def remove_container(docker_client, container_name):
    try:
        cur_container = docker_client.containers.get(container_name)
        cur_container.remove(v=True, force=True)
        return True
    except docker.errors.NotFound:
        logger.error(f'container for stop with name {container_name} not found')
        return False
    except docker.errors.APIError as de:
        logger.error(f'error while remove container {container_name}')
        logger.error(de)
        return False


def stop_and_rm_container(docker_client, container_name):
    # get container
    cur_container = get_container(docker_client, container_name)

    # get container status
    if not cur_container:
        logger.info(f'container {container_name} not found')
        return 'deleted'
    else:
        status = cur_container.status
        cont_id = cur_container.id
        logger.info('status', status, type(status))

    if status == 'running':
        logger.info(f'container {container_name} started already. Stop it!')
        # stop
        stop_result = stop_container(docker_client, cont_id)
        logger.info('stoped', stop_result)
        status = 'exited'
    else:
        logger.info("status not running")

    if status == 'exited':
        logger.info(f'container {container_name} exists already. Remove it!')
        # rm
        remove_result = remove_container(docker_client, cont_id)
        logger.info('removed, remove_result is ', remove_result)
        status = 'deleted'
    else:
        logger.info("status not exited")
    return status


def image_find_and_rm(docker_client, image_tag):
    cur_img = get_image(docker_client, image_tag)
    logger.info(cur_img)
    if cur_img:
        logger.info(f'image {image_tag} exists')
        logger.info(f'cur_img is {cur_img}, ID is {cur_img.id}')
        del_result = delete_image(docker_client, image_tag)
        logger.info(f'del_result of image {del_result}')
        return del_result
    else:
        # не нужно ничего удалять, контейнера нет
        return True


def create_image_and_container_by_dockerfile(
        docker_client: docker.DockerClient,
        path,
        image_tag,
        container_name,
        port
):
    # should be deleted
    status = stop_and_rm_container(docker_client, container_name)

    cur_cont = get_container(docker_client, container_name)
    if cur_cont:
        logger.error(f'container not deleted, {cur_cont}')
        sys.exit()

    # remove image
    if status == 'deleted':
        # remove image
        del_result = image_find_and_rm(docker_client, image_tag)
        if del_result:
            # create new image
            image, logs = docker_client.images.build(
                path=path,
                tag=image_tag,
                quiet=False,
                rm=True,        # creates image only without container
                forcerm=True,
                timeout=20
            )
            for log in logs:
                logger.debug(log)
            logger.info(f'image {image} created')

            # run container
            try:
                container = docker_client.containers.run(image_tag,
                                                         name=container_name,
                                                         detach=True,
                                                         ports={8080: port})
                for log in container.logs():
                    logger.debug(log)
                logger.info(f'container {container} created')

                i = 0
                while True:
                    i += 1
                    # logger.info(get_container_with_status(docker_client, container_name))
                    container.reload()
                    logger.info(f'container.status {container.status}')
                    if container.status == 'running':
                        break

                    if i == cfg.docker_n_iters:
                        logger.error(f'container {container_name}'
                                     f' can`t start,'
                                     f' status is {container.status}')
                        sys.exit()
                    time.sleep(cfg.docker_wait_on_iter)

            except docker.errors.APIError as api_e:
                logger.error(f'eroror while run container {container_name}')
                logger.error(str(api_e))
                sys.exit()
        else:
            logger.error(f'error while del image {image_tag}')
            sys.exit()
