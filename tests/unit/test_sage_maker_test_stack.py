import aws_cdk as core
import aws_cdk.assertions as assertions

from sage_maker_test.sage_maker_test_stack import SageMakerTestStack

# example tests. To run these tests, uncomment this file along with the example
# resource in sage_maker_test/sage_maker_test_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = SageMakerTestStack(app, "sage-maker-test")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
