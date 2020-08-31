![image](https://user-images.githubusercontent.com/21345604/91678118-53d99900-eb4d-11ea-9d56-ac8242380b89.png)

# Py-Blender-Room
A python framework for building 3D environments using Blender.

## Motivation
I once had a need to create a 3D model of an empty room. The model would consist of some walls with windows, a floor and a ceiling.
It was chosen to build it using Blender (https://www.blender.org/) a beautiful cross-platform and free 3D software.
Moreover, I chose not to create a model "with a mouse", but to program it with Blender's python API.

As a result, py-blender-room was born, hence the "room" in the name.

## How To

py-blender-room offers a workflow to create models and open them in blender.
Individual models, called `projects`, reside in `projects` package. 

The initial project, named `room1`, can be found there. The more models I (or anyone else) need to create, the more sub-packages will appear there.

![image](https://user-images.githubusercontent.com/21345604/91678617-b1221a00-eb4e-11ea-8974-eb3c6db54ed0.png)

the entry script of the project is `build.py` and it is meant to be interpreted with Blender's built-in Python, as follows:

`~/dist/blender-2.83.4-linux64/blender --python py_blender_room/projects/room1/production_build.py`

as a result, blender will open with the model as shown in the video below:

![open_blender](https://user-images.githubusercontent.com/21345604/91690972-83999880-eb6f-11ea-8068-895f2c8d218e.gif)

**tip:** if you simply want to validate your script without opening Blender's User Interface, you may run Blender with `-b` option.

## Architecture

![image](https://user-images.githubusercontent.com/21345604/91696816-d461bf00-eb78-11ea-97cf-ea7e76d24990.png)

- `Scene` holds some objects
- `SceneRenderer` knows how to get those objects and make `Modeler` "materialize" them
- `Modeler` is something that implements `ModelerInterface`. An  example of a `Modeler` is `Blender`. Another example is `FakeModeler` which is used in unit test.

### What a project is?

- a scene class
- a scene renderer class
- build.py script 

each of these files is described below:

### A scene class
This class, inheriting from `Scene`, defines a high-level list of objects.

**Objects can be anything**: in case of Room1 project, they are "Wall", "Floor" etc. In case of other imaginary projects,
they could be "Tree", "Road" and so on. 

In a sense, these classes define the domain-specific language you need for your particular project.

The `Scene`, in its turn, maintains the list of objects, i.e. those "Walls", "Trees" and "Roads"

The only requirement is that your scene renderer (described in the following section), knows how to translate the objects 
 the scene consists of, into the underlying `modeler` instruction. 
For example, in case of walls, Room1SceneRenderer knows how to make modeler create Box meshes,
cut out windows, insert "glasses" ang put the whole ensemble into appropriate position.

### A Scene Renderer Class

Your scene renderer class is a middleware that translates your domain-specific scene objects into instructions modeler understands.

A Modeler is "something" that can build your model, for example, Blender's API is modeler. In the framework, modeler is 
represented with a class implementing `ModelerInterface`.

**note:** if you want to use certain feature of blender that wasn't used before, you might want to extend that interface. 


### build.py

This is an entry script:

```python
def run():
    scene = Room1Scene()
    scene.build()
    modeler = Blender()
    scene_renderer = Room1SceneRenderer()
    scene_renderer.modeler = modeler
    scene_renderer.render(scene)
```
above is a real working example from `Room1` project.

The build script:
- instantiates a scene
- invokes a `build` method of the scene
- creates a modeler
  - for Blender, just use `Blender()`
- instantiates a scene renderer
- connects a scene renderer with a modeler
- renders the scene