import aws_cdk as cdk

from infra.stacks.playground import PGStack
from infra.stacks.prod_stack import ProdStack

app = cdk.App()

ProdStack(app)
PGStack(app)
app.synth()
