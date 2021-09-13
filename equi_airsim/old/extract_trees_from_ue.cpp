#include "EngineUtils.h"
#include "Runtime/Foliage/Public/InstancedFoliageActor.h"

for (TActorIterator<AInstancedFoliageActor> ActorItr(GetWorld()); ActorItr; ++ActorItr)
    {
        AInstancedFoliageActor* FoliageMesh = *ActorItr;

        for (auto& MeshPair : FoliageMesh->FoliageMeshes)
        {
            const FFoliageMeshInfo& MeshInfo = *MeshPair.Value;
            UHierarchicalInstancedStaticMeshComponent* MeshComponent = MeshInfo.Component;
            TArray<FInstancedStaticMeshInstanceData> MeshDataArray = MeshComponent->PerInstanceSMData;
            FString MeshName = MeshComponent->GetStaticMesh()->GetName();

            for (auto& MeshMatrix : MeshDataArray)
            {
                FTransform MeshTransform = FTransform(MeshMatrix.Transform);

                UE_LOG(LogTemp, Warning, TEXT("%s, %f, %f, %f, %f, %f, %f, %f, %f, %f,"),
                    *MeshName,
                    MeshTransform.GetLocation().X,
                    MeshTransform.GetLocation().Y,
                    MeshTransform.GetLocation().Z,
                    MeshTransform.GetRotation().X,
                    MeshTransform.GetRotation().Y,
                    MeshTransform.GetRotation().Z,
                    MeshTransform.GetScale3D().X,
                    MeshTransform.GetScale3D().Y,
                    MeshTransform.GetScale3D().Z);
            }
        }
    }