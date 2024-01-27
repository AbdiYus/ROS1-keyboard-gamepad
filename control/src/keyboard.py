import rospy 
from std_msgs.msg import Int32
from pynput import keyboard
from pynput.keyboard import Key

def on_key_press(key):
    global running
    if key == Key.up:
        publish_key(key, 1)
    elif key == Key.down:
        publish_key(key, 2)
    elif key == Key.left:
        publish_key(key, 3)
    elif key == Key.right:
        publish_key(key, 4)
    elif key == Key.esc:
        rospy.signal_shutdown("shutdown")
        running = False 
    

def publish_key(key, inp):
    global pub
    rospy.loginfo(f"key pressed {key}")
    pub.publish(inp)

def release_key(key):
    global pub 
    pub.publish(0)

running = True
pub = rospy.Publisher("keyboard", Int32, queue_size=10)
listener = keyboard.Listener(on_press=on_key_press, on_release=release_key)
listener.start()

try:
    rospy.init_node("keyboard")
    while running:
        pass
except rospy.ROSInterruptException:
    pass