from pyassimp import load, export

with load("scene.fbx") as scene:
    assert len(scene.meshes)
    mesh = scene.meshes[0]

    assert len(mesh.vertices)
    print(mesh.vertices[0])

    # export(scene, "bunny.pbrt", "pbrt")
