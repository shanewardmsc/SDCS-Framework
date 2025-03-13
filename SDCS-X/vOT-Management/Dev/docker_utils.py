import docker
import docker.errors

# -------------------------------------------------------#
#               Docker Interface for services            #
# -------------------------------------------------------#
class DockerInterface:
    # Class for creating Docker client interface

    def __init__(self):
        pass

    def docker_connect(self):
        # Create and return a Resource
        try:
            client = docker.from_env()
            if client is not None:
                return client
            else:
                print("Error: docker_utils() client connection failed")
                return

            return client

        except docker.errors.APIError as error:
            print("Error: docker_utils() ", str(error))
            return
        except Exception as error:
            print("Error: docker_utils() General exception occurred: ", str(error))
            return


# -------------------------------------------------------#
#         Docker Controller Interface for services       #
# -------------------------------------------------------#
class DockerController:

    def __init__(self, client):
        self.client = client

    def list_all_containers(self):
        try:
            # Obtain list of all containers
            all_containers = self.client.containers.list(all=True)
            cont_idx = 0

            # Loop through all docker containers
            for cont in all_containers:
                # Print list of each container with ID
                print("Container ID: ", cont_idx, cont)
                cont_idx += 1

            if cont_idx == 0:
                print("Error: docker_utils() No containers found")

            return all_containers

        except TypeError as error:
            print("Error: docker_utils() ", str(error))
            return
        except docker.errors.APIError as error:
            print("Error: docker_utils() ", str(error))
            return
        except Exception as error:
            print("Error: docker_utils() ", str(error))
            return

    def list_stopped_containers(self):
        # Start instance with id 'instance_id'
        try:
            all_stopped_containers = self.client.containers.list(filters={'status': 'exited'})
            cont_idx = 0

            for cont in all_stopped_containers:
                print("Container ID: ", cont_idx, cont)
                cont_idx += 1

            return all_stopped_containers

        except docker.errors.APIError as error:
            print("Error: docker_utils() ", str(error))
            return
        except Exception as error:
            print("Error: docker_utils() ", str(error))
            return

    def list_running_containers(self):
        # Start instance with id 'instance_id'
        try:
            all_stopped_containers = self.client.containers.list(filters={'status': 'running'})
            cont_idx = 0

            for cont in all_stopped_containers:
                print("Container ID: ", cont_idx, cont)
                cont_idx += 1

        except docker.errors.APIError as error:
            print("Error: docker_utils() ", str(error))
            return
        except Exception as error:
            print("Error: docker_utils() ", str(error),)
            return

    def run_container(self, image):
        # Start instance with id 'instance_id'
        try:
            run_container = self.client.containers.run(image, detach=True)
            print("Container: ", str(run_container), " running")

        except docker.errors.ContainerError as error:
            print("Error: docker_utils() ", str(error))
            return
        except docker.errors.ImageNotFound as error:
            print("Error: docker_utils() ", str(error))
            return
        except docker.errors.APIError as error:
            print("Error: docker_utils() ", str(error))
            return
        except Exception as error:
            print("Error: docker_utils() ", str(error))
            return

    def exec_cmd_container(self, container, command):
        # Start instance with id 'instance_id'
        try:
            execute_command = self.client.containers.run(container, command, detach=True)
            print("Command: ", str(command), " executed on container: ", str(command))

        except docker.errors.ContainerError as error:
            print("Error: docker_utils() ", str(error))
            return
        except docker.errors.ImageNotFound as error:
            print("Error: docker_utils() ", str(error))
            return
        except docker.errors.APIError as error:
            print("Error: docker_utils() ", str(error))
            return
        except Exception as error:
            print("Error: docker_utils() ", str(error))
            return

    def view_port_mappings(self, container):
        try:
            container = self.client.containers.get(container)
            print("Container ports: ", str(container.ports))

        except docker.errors.APIError as error:
            print("Error: docker_utils() ", str(error))
            return
        except Exception as error:
            print("Error: docker_utils() ", str(error))
            return

    def remove_all_containers(self):
        try:
            delete_containers = self.client.containers.prune(filters={'status': 'exited'})
            print("Containers stopped and removed")

        except docker.errors.APIError as error:
            print("Error: docker_utils() ", str(error))
            return
        except Exception as error:
            print("Error: docker_utils() ", str(error))
            return

    def list_all_images(self):
        try:
            images = self.client.images.list()
            img_idx = 0

            for img in images:
                print("Image ID: ", img_idx, img)
                img_idx += 1

        except docker.errors.APIError as error:
            print("Error: docker_utils() ", str(error))
            return
        except Exception as error:
            print("Error: docker_utils() ", str(error))
            return

    def save_container_image(self, image):
        try:
            image = self.client.images.get(image)
            file_location = "/tmp/" + str(image) + ".tar"
            file = open(file_location, 'wb')
            for chunk in image.save():
                file.write(chunk)
            file.close()

        except docker.errors.APIError as error:
            print("Error: docker_utils() ", str(error))
            return
        except Exception as error:
            print("Error: docker_utils() ", str(error))
            return

    def build_container_image(self, path, dockerfile, tag):
        try:
            image = self.client.images.build(
                path=path,
                dockerfile=dockerfile,
                tag=tag)

        except docker.errors.APIError as error:
            print("Error: docker_utils() ", str(error))
            return
        except Exception as error:
            print("Error: docker_utils() ", str(error))
            return
