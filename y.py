class Super():
    
    def get_child_prop(self):
        prop = getattr(self, 'prop')
        print(prop)

class Child(Super):
    def __init__(self):
        self.prop = 'child prop'
        self.get_child_prop()
    
child = Child()