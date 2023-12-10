```bash
roslaunch ur_gazebo ur5_bringup.launch
```

```bash
roslaunch ur5_moveit_config moveit_planning_execution.launch sim:=true
``````

```bash
python main.py gcode_files/vase.gcode
```