import airsim
import argparse
from IPython.display import display

PARSER = argparse.ArgumentParser()

def main():
    """Run main function and handle airsim client."""
    client.confirmConnection()
    display('Objects present in the environment : ')
    for i in  sorted(client.simListSceneObjects()):
        print(i)
    #display('simGetMeshPositionVertexBuffers :\n', client.simGetMeshPositionVertexBuffers())

if __name__ == '__main__':
    args = PARSER.parse_args()
    client = airsim.VehicleClient()
    main()