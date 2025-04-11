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
            all_containers = self.client.containers.list(all=True)

            # Filter out containers with status 'exited' and 'running'
            filtered_containers = [container for container in all_containers if container.status not in ['exited', 'running']]

            cont_idx = 0

            # Loop through all docker containers
            for cont in filtered_containers:
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

    def list_ot_containers(self):
        try:
            # Define the filter for containers with label domain="ot_domain"
            filters = {"label": "domain=OT_DOMAIN"}

            # List all containers with the filter applied
            ot_containers = self.client.containers.list(all=True, filters=filters)

            cont_idx = 0

            # Loop through all filtered containers
            for cont in ot_containers:
                # Print list of each container with ID
                print(f"Container ID: {cont_idx}, Name: {cont.name}, ID: {cont.id}, Status: {cont.status}")
                cont_idx += 1

            if cont_idx == 0:
                print("Error: No containers found with label 'domain=ot_domain'")

            return ot_containers

        except TypeError as error:
            print(f"Error: {str(error)}")
            return
        except docker.errors.APIError as error:
            print(f"Error: {str(error)}")
            return
        except Exception as error:
            print(f"Error: {str(error)}")
            return
            
    def list_it_containers(self):
        try:
            # Define the filter for containers with label domain="it_domain"
            filters = {"label": "domain=IT_DOMAIN"}

            # List all containers with the filter applied
            it_containers = self.client.containers.list(all=True, filters=filters)

            cont_idx = 0

            # Loop through all filtered containers
            for cont in it_containers:
                # Print list of each container with ID
                print(f"Container ID: {cont_idx}, Name: {cont.name}, ID: {cont.id}, Status: {cont.status}")
                cont_idx += 1

            if cont_idx == 0:
                print("Error: No containers found with label 'domain=it_domain'")

            return it_containers

        except TypeError as error:
            print(f"Error: {str(error)}")
            return
        except docker.errors.APIError as error:
            print(f"Error: {str(error)}")
            return
        except Exception as error:
            print(f"Error: {str(error)}")
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
            all_running_containers = self.client.containers.list(filters={'status': 'running'})
            cont_idx = 0

            for cont in all_running_containers:
                print("Container ID: ", cont_idx, cont)
                cont_idx += 1
            
            return all_running_containers
            
        except docker.errors.APIError as error:
            print("Error: docker_utils() ", str(error))
            return
        except Exception as error:
            print("Error: docker_utils() ", str(error),)
            return


    def run_container(self, image):
        try:
            # Start the container using the given image
            run_container = self.client.containers.run(image, detach=True)
            print(f"Container {run_container.id} started successfully.")
            return run_container.id  # Return the container ID after starting the container
        except docker.errors.ContainerError as error:
            print(f"Error: docker_utils() {str(error)}")
            return None
        except docker.errors.ImageNotFound as error:
            print(f"Error: docker_utils() Image {image} not found.")
            return None
        except docker.errors.APIError as error:
            print(f"Error: docker_utils() {str(error)}")
            return None
        except Exception as error:
            print(f"Error: docker_utils() {str(error)}")
            return None


    def restart_container(self, container_id):
        try:
            container = self.client.containers.get(container_id)
            if container.status == "exited":
                container.start()
                print(f"Container {container_id} restarted successfully.")
            else:
                print(f"Container {container_id} is already running.")
            return container.id
            
        except docker.errors.NotFound:
            print(f"Error: Container {container_id} not found.")
            return None
        except docker.errors.APIError as error:
            print(f"Error: {str(error)}")
            return None
        except Exception as error:
            print(f"Unexpected error: {str(error)}")
            return None


    def stop_container(self, container_id):
        # Stop a container given its ID
        try:
            container = self.client.containers.get(container_id)
            container.stop()
            print(f"Container {container_id} stopped successfully.")
        except docker.errors.NotFound as error:
            print(f"Error: docker_utils() Container {container_id} not found.")
        except docker.errors.APIError as error:
            print(f"Error: docker_utils() API error: {str(error)}")
        except Exception as error:
            print(f"Error: docker_utils() General exception occurred: {str(error)}")

    
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


    def view_port_mappings(self, container_name):
        try:
            container = self.client.containers.get(container_name)
            port_mappings = container.ports
            
            # Initialize a dictionary to store port mappings
            port_mapping_info = {}
            
            if port_mappings:
                for port, mappings in port_mappings.items():
                    if mappings:  # Check if mappings is not None
                        host_info = []
                        for mapping in mappings:
                            host_ip = mapping.get('HostIp', 'Not Available')
                            host_port = mapping.get('HostPort', 'Not Available')
                            host_info.append(f"Host IP: {host_ip}, Host Port: {host_port}")
                        port_mapping_info[port] = host_info
                    else:
                        port_mapping_info[port] = ["Not mapped to any host port."]
            else:
                port_mapping_info["No Ports"] = ["No ports are mapped."]
            
            return port_mapping_info
                
        except docker.errors.APIError as error:
            print(f"Error fetching container info: {str(error)}")
            return {"Error": str(error)}
        except Exception as error:
            print(f"Unexpected error: {str(error)}")
            return {"Error": str(error)}


    def remove_container(self, container_id):
        try:
            container = self.client.containers.get(container_id)
            container.remove(force=True)
            print(f"Container {container_id} removed successfully.")
        except docker.errors.NotFound as error:
            print(f"Error: docker_utils() Container {container_id} not found.")
        except docker.errors.APIError as error:
            print(f"Error: docker_utils() API error: {str(error)}")
        except Exception as error:
            print(f"Error: docker_utils() General exception occurred: {str(error)}")


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

            return images

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
