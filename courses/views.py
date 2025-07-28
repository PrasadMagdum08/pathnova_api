from rest_framework.views import APIView
from rest_framework.response import Response
from .authentication import NodeJWTAuthentication
from .models import student_profiles_collection, courses_collection


def refine_skills_with_llm(goals, specialization):
    """
    Simulated LLM-based skill refinement from goals and specialization.
    Replace this with actual GenAI model calls later.
    """
    combined_context = f"{specialization.lower()} {' '.join(goals).lower()}"

    if "ai" in combined_context or "ml" in combined_context:
        skills = [
            "machine learning", "data structures", "python", "neural networks",
            "deep learning", "model evaluation", "math for ML"
        ]
    elif "web" in combined_context or "frontend" in combined_context:
        skills = ["javascript", "react", "html", "css", "web development"]
    elif "backend" in combined_context or "system" in combined_context:
        skills = ["system design", "node.js", "databases", "api design"]
    else:
        skills = goals


    # Prioritize user-specified goals
    ranked_skills = sorted(skills, key=lambda x: (x not in goals, x))
    return skills, ranked_skills


class CourseRecommendationView(APIView):
    authentication_classes = [NodeJWTAuthentication]

    def get(self, request):
        email = getattr(request.user, "email", None)
        if not email:
            return Response({"error": "Email not found in token"}, status=401)

        student = student_profiles_collection.find_one({"email": email})
        if not student:
            return Response({"error": "Student profile not found"}, status=404)

        specialization = student.get("intended_specialized_major", "").strip().lower()
        goals = [g.strip().lower() for g in student.get("upskilling", []) if isinstance(g, str)]
        max_duration = int(student.get("portfolio_building_duration", 12))

        print("Specialization:", specialization)
        print("Goals:", goals)
        print("Max Duration:", max_duration)

        # LLM refinement logic
        skills, ranked_skills = refine_skills_with_llm(goals, specialization)
        print("Refined skills:", skills)
        print("Ranked skills:", ranked_skills)

        # Updated MongoDB query
        query = {
            "$and": [
                {"goals": {"$in": ranked_skills}},
                {"duration_weeks": {"$lte": max_duration}}
            ]
        }

        courses = list(courses_collection.find(query, {"_id": 0}))
        print(f"Matched {len(courses)} courses for {email}")

        if not courses:
            return Response({
                "email": email,
                "total": 0,
                "recommendations": [],
                "message": "No matching courses found. Please update your goals or specialization."
            }, status=200)

        # Optionally sort by relevance (based on ranked skills)
        def score(course):
            goal_matches = sum(skill in [g.lower() for g in course.get("goals", [])] for skill in ranked_skills)
            return goal_matches

        sorted_courses = sorted(courses, key=score, reverse=True)

        return Response({
            "email": email,
            "total": len(sorted_courses),
            "recommendations": sorted_courses
        }, status=200)
