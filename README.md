# ROS1-keyboard-gamepad
A ROS node designed to capture input from a keyboard or a PS5 gamepad and publish it to a specified ROS topic.
## Installing 
The keyboard node uses the pynput library.  
```
pip install pynput
```
And the gamepad node uses the pygame library. 
```
pip install pygame
```
## Topic 
The keyboard publishes to the topic "keyboard" as __Int32__

The gamepad publishes to the topic "controller" as an __Float32MultiArray__