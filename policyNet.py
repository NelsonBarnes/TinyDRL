from tinygrad import Tensor


class policyNet:
    def __init__(self, input_dim, output_dim):
        hidden_dim = input_dim * 10 # TODO: make this an arg
        self.l1 = Tensor.kaiming_uniform(input_dim, hidden_dim)
        self.l2 = Tensor.kaiming_uniform(hidden_dim, hidden_dim)
        self.l3 = Tensor.kaiming_uniform(hidden_dim, output_dim)

    def __call__(self, x:Tensor):
        return x.flatten(1).dot(self.l1).relu().dot(self.l2).relu().dot(self.l3).softmax().squeeze()    

           

    
