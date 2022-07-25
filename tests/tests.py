from unittest import TestCase

# #Dummy test data taken from Springboard's test file.
# CUPCAKE_DATA = {
#     "flavor": "TestFlavor",
#     "size": "TestSize",
#     "rating": 5,
#     "image": "http://test.com/cupcake.jpg"
# }

# CUPCAKE_DATA_2 = {
#     "flavor": "TestFlavor2",
#     "size": "TestSize2",
#     "rating": 10,
#     "image": "http://test.com/cupcake2.jpg"
# }

# CUPCAKE_DATA_3 = {
#     "flavor": "TestFlavor3",
#     "size": "TestSize3",
#     "rating": 3,
#     "image": "http://test.com/cupcake3.jpg"
# }

# class CupcakeAPITesting(TestCase):
#     def setUp(self):
#         Cupcakes.query.delete()

#         cupcake_1 = Cupcakes(**CUPCAKE_DATA)
#         cupcake_2 = Cupcakes(**CUPCAKE_DATA_2)

#         db.session.add_all([cupcake_1,cupcake_2])
#         db.session.commit()

#         self.cupcake1 = cupcake_1
#         self.cupcake2 = cupcake_2

#     def tearDown(self):
#         db.session.rollback()

#     def test_get_cupcakes(self):
#         #Make GET request to API, then search for JSON info.
#         with app.test_client() as client:
#             response = client.get('/api/cupcakes')
#             self.assertEqual(response.status_code,200)
#             self.assertEqual(response.json,
#             {   "cupcakes": [{
#                 "id": self.cupcake1.id,
#                 "flavor": "TestFlavor",
#                 "size": "TestSize",
#                 "rating": 5,
#                 "image": "http://test.com/cupcake.jpg"
#             },
#             {   "id": self.cupcake2.id,
#                 "flavor": "TestFlavor2",
#                 "size": "TestSize2",
#                 "rating": 10,
#                 "image": "http://test.com/cupcake2.jpg"
#             }]
#             })
    