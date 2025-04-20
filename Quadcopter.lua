sim=require'sim'

function sysCall_init() 
    -- Detatch the manipulation sphere:
    targetObj=sim.getObject('../target')
    sim.setObjectParent(targetObj,-1,true)
    
    d=sim.getObject('../base')
    heli=sim.getObject('..')
    
    -- Create a simple rectangle
    rectSize = {0.3, 0.3, 0.01} -- width, length, height
    rectPosition = {0, 0, 0.1} -- x, y, z position
    rectColor = {0.2, 0.6, 0.8, 0} -- RGB + transparency
    
    -- Create rectangle as a cuboid
    rectangle = sim.createPrimitiveShape(sim.primitiveshape_cuboid, rectSize)
    sim.setObjectPosition(rectangle, d, rectPosition)
    sim.setShapeColor(rectangle, nil, sim.colorcomponent_ambient_diffuse, rectColor)
    
    -- Make it a child of the base
    sim.setObjectParent(rectangle, d, true)
    
    -- Set object name/alias
    sim.setObjectAlias(rectangle, "SimpleRectangle")
end

function sysCall_cleanup() 
    -- Nothing to clean up
end 

function sysCall_actuation() 
    -- Basic position control to follow target
    targetPos=sim.getObjectPosition(targetObj)
    pos=sim.getObjectPosition(d)
    
    -- Simple height control
    heightDiff = targetPos[3] - pos[3]
    thrust = 5.45 + heightDiff * 2
    
    -- Apply force to move toward target
    force = {0, 0, thrust}
    sim.addForce(d, {0, 0, 0}, force)
end