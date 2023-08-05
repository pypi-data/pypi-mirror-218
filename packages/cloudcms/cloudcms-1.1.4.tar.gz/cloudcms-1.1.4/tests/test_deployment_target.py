from .abstract_test import AbstractTest

class TestDeploymentTarget(AbstractTest):

    def test_deployment_target(self):
        platform = type(self).platform

        deployment_target_id = platform.create_deployment_target({ 
            'type': 's3',
            'config': {
                'accessKey': 'abc',
                'secretKey': 'abc',
                'region': 'us-east-1',
                'bucketName': 'abc',
                'prefix': 'abc'
            }
        })
        
        self.assertIsNotNone(deployment_target_id)

        deployment_target = platform.read_deployment_target(deployment_target_id)
        self.assertIsNotNone(deployment_target)

        try:
            all_deployment_targets = platform.list_deployment_targets()
            self.assertGreater(len(all_deployment_targets), 0)

            queried_deployment_targets = platform.query_deployment_targets({ 'type': 's3'})
            self.assertGreater(len(queried_deployment_targets), 0)

            deployment_target.data['config']['accessKey'] = 'def'
            deployment_target.update()

            deployment_target.reload()
            self.assertEqual('def', deployment_target.data['config']['accessKey'])

            # deployment_target.delete()
            # deployment_target = platform.read_deployment_target(deployment_target_id)
            # self.assertIsNone(deployment_target)

        except Exception as err:
            # deployment_target.delete()
            raise err


