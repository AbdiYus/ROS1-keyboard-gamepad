import pygame 
import rospy
from std_msgs.msg import Float32MultiArray 

class ds5:
    def __init__(self):
        pygame.joystick.init()

        self.joystick = pygame.joystick.Joystick(0) # First joystick
        self.joystick.init()
        self.axis_states = [0, 0, -1, 0, 0, -1]  # Initialize axis states to their default values.
        self.trigger_states = [0, 0]  # Initialize trigger states to their default values.
        self.face_buttons = [0, 0, 0, 0]  # Initialize face button states to their default values.
    
    def get_specific_axis(self, event, event_axis):
        dead_zone = 0.05
        if event.type == pygame.JOYAXISMOTION:
            if event.axis == event_axis:
                axis_position = self.joystick.get_axis(event.axis)
                if abs(axis_position) > dead_zone and abs(axis_position) > 0.3:
                    self.axis_states[event_axis] = round(axis_position, 2)  # Update the state of the axis.
                else:
                    self.axis_states[event_axis] = 0
        return self.axis_states[event_axis]  # Return the current state of the axis.
    
    def get_Triggerbutton(self, event, event_button):
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == event_button:
                self.trigger_states[event_button - 4] = 1
        elif event.type == pygame.JOYBUTTONUP:
            if event.button == event_button:
                self.trigger_states[event_button - 4] = 0
        return self.trigger_states[event_button - 4]
    
    def get_facebutton(self, event, event_button):
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == event_button:
                self.face_buttons[event_button] = 1
        elif event.type == pygame.JOYBUTTONUP:
            if event.button == event_button:
                self.face_buttons[event_button] = 0
        return self.face_buttons[event_button]

    def get_triggers(self, event):
        triggers = [self.get_Triggerbutton(event, i) for i in range(4,6)]
        return triggers
    
    def get_facebuttons(self, event):
        facebuttons = [self.get_facebutton(event, i) for i in range(4)]
        return facebuttons
            
    def get_axis(self, event):
        axes = [self.get_specific_axis(event, i) for i in range(6)]
        return axes
    
    def rumble(self, inp):
        add = inp*10
        self.joystick.rumble(10, (10*add), 100)
    
##############################MAIN#####################################
pygame.init()
controller = ds5()

def publish_data(data, pub):
    rospy.loginfo(f"data: {data}")
    pub.publish(data)

running = True
pub = rospy.Publisher("controller", Float32MultiArray, queue_size=10)
prev_data = None 

try:
    rospy.init_node("controller")
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
            axes = controller.get_axis(event)
            triggers = controller.get_triggers(event)  
            face_buttons = controller.get_facebuttons(event)

            if face_buttons[2] == 1:
                running = False
            
            data = Float32MultiArray()
            data.data = axes + triggers + face_buttons

            if data.data != prev_data:
                publish_data(data, pub)
                prev_data = data.data
                
            
        if axes[5] > 0.3:
            controller.rumble(axes[5])
       
        pass   

except rospy.ROSInterruptException:
    pass