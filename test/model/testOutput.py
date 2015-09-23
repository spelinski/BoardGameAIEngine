import unittest
from battleline.model.Output import Output, ACTIONS, COLORS, TACTICS
class TestOutput(unittest.TestCase):

    def setUp(self):
        self.output = Output()

    def test_output_all_actions_function(self):
		actionList = [	("p1",ACTIONS[0],1,COLORS[0],"",0),
						("p1",ACTIONS[1],0,COLORS[0],TACTICS[0],0),
						("p1",ACTIONS[1],2,COLORS[1],"",0),
						("p1",ACTIONS[1],0,COLORS[0],TACTICS[1],0),
						("p1",ACTIONS[2],0,COLORS[0],"",1),
						("p1",ACTIONS[3],0,COLORS[0],"",0) 
					]
		for name,action,number,color,tactic,flag in actionList:
			#=act
			self.assertTrue(self.output.action(name,action,number,color,tactic,flag))

