from my_app.models import FeedbackCategory, FeedbackQuestion

# Define feedback categories and questions
categories = {
    "Overall Impressions": [
        "What was your overall impression of the story?",
        "Did the book seem too long or too short?",
        "What didn’t make sense to you?",
        "Did you feel like you knew this place and time? Were there enough sensory details to sweep you away?"
        "What parts did you like best?",
        "What parts did you like least?",
    ],
    "Plot": [
        "Did the story grab you at the beginning?",
        "Were there any points where you started to lose interest?",
        "Was the story easy to follow? If not, why not?",
        "Was there anything particular that you found confusing?",
        "Was there anything that you had trouble believing or that seemed illogical?",
        "Did you find any plot holes or inconsistencies?",
        "Was the plot fulfilled in a satisfying way? In other words, was the ending satisfying?",
    ],
    "Characters": [
        "Did you find the main character engaging? If so, what was most engaging about them? If you didn’t find them engaging, why not?",
        "Was the main character relatable? What did you like about him/her? What didn't you like?",
        "Were the protagonist’s goals clear?",
        "Which character was your favorite, and why",
        "Which character was your least favorite, and why?",
        "Which character(s) do you wish was developed more?",
        "Were you able to keep track of the characters, i.e. who was who? Were there too many? Too few?",
    ],
    "Pacing": [
        "Were there any places the story moved too quickly or too slowly?",
        "Were there any scenes that dragged or were boring?",
        "Were there any scenes that you wished were expanded?",
    ],
    "Dialogue": [
        "Did the dialogue sound realistic? If not, where did it sound fake?",
        "Were the dialogue tags 'invisible' or did they pull you from the story?",
        "Was there anything you disliked? If so, what?",
    ],
    "Description": [
        "Were you able to visualize the setting for every scene? If not, where could more description be given?",
        "Were you able to visualize every important character? If not, who could use more description?",
    ],
    "Craft": [
        "Was the narrative voice consistent throughout the course of the novel?",
        "Where there any overused words or phrases?",
    ],
    "Other": [
        "What was your favorite scene/chapter, and why?",
        "What was your least favorite scene/chapter, and why?",
        "Did you feel immersed in the story? If not, where are places you couldn't 'suspend disbelief?'",
        "What are your thoughts about the ending?",
        "What were the strengths of this novel? What were the weaknesses?",
    ],
}

for category_name, questions in categories.items():
    category, created = FeedbackCategory.objects.get_or_create(name=category_name)
    for question_text in questions:
        FeedbackQuestion.objects.get_or_create(
            category=category, question_text=question_text
        )
