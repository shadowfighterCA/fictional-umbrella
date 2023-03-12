import grpc
from concurrent import futures
import random
from recommendations_pb2 import (BookCategory,
                                RecommendationResponse,
                                BookRecommendation
                                 )

import recommendations_pb2_grpc

books_by_category = {

    BookCategory.MYSTERY :[
        BookRecommendation(id=1,title="And Then There Were None"),
        BookRecommendation(id=2,title="The Big Sleep by Raymond"),
        BookRecommendation(id=3,title="Gone Girl by Gillian Flynn"),
        BookRecommendation(id=4,title="The Postman Always Rings Twice"),
        BookRecommendation(id=5,title="In Cold Blood"),
    ],

    BookCategory.SCIENCE_FICTION:[
        BookRecommendation(id=6,title="Del Rey Snow Crash"),
        BookRecommendation(id=7,title="Gallery Books Contact"),
        BookRecommendation(id=8,title="Voyager A Canticle for Leibowitz"),
        BookRecommendation(id=9,title="Mariner Books Solaris"),
        BookRecommendation(id=10,title="Ace Neuromancer"),
    ],

    BookCategory.SELF_HELP:[
        BookRecommendation(id=11,title="Atomic Habits"),
        BookRecommendation(id=12,title="How to Win Friends and Influence People"),
        BookRecommendation(id=13,title="The 7 Habits of Highly Effective People"),
        BookRecommendation(id=14,title="The Power of Habit: Why We Do What We Do in Life and Business"),
        BookRecommendation(id=15,title="The Life-Changing Magic of Tidying Up"),
    ],



}


class RecommendationService(recommendations_pb2_grpc.RecommendationsServicer):
    def Recommend(self, request, context):
        if request.category not in books_by_category:
            context.abort(grpc.Statuscode.NOT_FOUND,"Category not found")

        books_for_category = books_by_category[request.category]
        num_results = min(len(books_for_category),request.max_results)
        books_to_recommend = random.sample(books_for_category,num_results)

        return RecommendationResponse(recommendations= books_to_recommend)
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    recommendations_pb2_grpc.add_RecommendationsServicer_to_server(RecommendationService(),server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()









