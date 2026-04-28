import time
import random

# variables to store user's details and track their cooperation level
cooperative = 0
uncooperative = 0
evasive = 0


# array of questions and their corresponding wanted answers keywords
questions_why = {
    "low_pressure": ["Do you know why you're here today?"],
    "medium_pressure": ["Why were you near the location of the incident?"],
    "high_pressure": ["Your presence at the scene suggests intent. Explain your actions."]
}
keywords_why = ["reason", "cause", "motivation"]

questions_where = {
    "low_pressure": ["Where were you last night?"],
    "medium_pressure": ["Can you account for your whereabouts during the incident?"],
    "high_pressure": ["Your location during the crime is unverified. Explain it."]
}
keywords_where = ["home", "work", "school", "neighbor", "plans"]

questions_when = {
    "low_pressure": ["When did you arrive at the crime scene?"],
    "medium_pressure": ["Can you provide a timeline of your activities during the time of the crime?"],
    "high_pressure": ["Your timeline of events is inconsistent with the evidence. Explain it."]
}
keywords_when = ["arrive", "leave", "time", "when", "before", "after", "pm", "am"]

questions_who = {
    "low_pressure": ["Who were you with last night?"],
    "medium_pressure": ["Can you provide the names of anyone you were with during the incident?"],
    "high_pressure": ["Your associations during the crime are suspicious. Explain them."]
}
keywords_who = ["with", "company", "acquaintance", "friend", "family"]

questions_final = {
    "low_pressure": ["Is there anything you want to clarify before we conclude?"],
    "medium_pressure": ["Is there any final information you think is relevant?"],
    "high_pressure": ["You have been quite uncooperative. You have one last opportunity to explain your actions."]
}
keywords_explanation = ["because", "since", "went", "was", "due to", "as a result of", "in order to", "so that", "reason", "with"] # same as the explanation keywords

# array of positive and negative affirmative keywords for questions
positive_answers = ["yes", "yeah", "yep", "sure", "correct", "right"]
negative_answers = ["no", "nope", "nah", "not", "incorrect", "wrong"]

# array of hostile/unhelpful keywords for questions
hostile_answers = ["don't have to", "none of your business", "refuse to answer", "not answering", "not telling you", "not saying", "not going to say", "not going to tell you"]
evasive_answers = ["have rights", "lawyer", "no comment", "don't know", "dont know", "not sure", "can't remember", "cant remember", "no idea", "can't recall", "cant recall", "not certain", "not positive", "not 100% sure", "no thanks", "not answering", "not telling you", "not saying", "not going to say", "not going to tell you", "not guilty", "innocent"]

# array of types of responses for each question
response_positive = ["That sounds good.", "I appreciate your cooperation.", "Thank you for your honesty.", "I see. That makes sense."]
response_evasive = ["I see.", "Okay.", "Alright.", "Hmm.", "Interesting."]
response_nuetral = ["Thank you for your answer.", "I understand.", "Noted."]
response_passive_aggressive = ["Are you sure about that?", "That doesn't sound right.", "I find that hard to believe.", "Is that so?"]
response_times_up = ["Time's up.", "You have run out of time.", "You took too long to answer.", "Your time is up."]
response_vague = [
    "Your previous statements raise questions.",
    "Your responses lack clarity.",
    "There are inconsistencies in your statements."
]


# function to ask a random question from a given list and check the user's answer for wanted keywords, hostile keywords, or unhelpful keywords
def ask_adaptive_question(question_list, keywords=None, time_limit=15):
    global cooperative, uncooperative, evasive

    officer_response = "Officer: "

    # determine the pressure level of the question based on the user's cooperation level, then pick a random question from the appropriate pressure level
    # also add a comment to the officer's response based on the user's cooperation level
    if uncooperative > 2:
        level = "high_pressure"
        officer_response += "Your lack of cooperation is concerning. "
    elif evasive > 2:
        level = "medium_pressure"
        officer_response += "Your responses are being recorded. "
    else:
        level = "low_pressure"

    officer_response += random.choice(question_list[level])
    print(officer_response)

    start_time = time.time()
    user_input = input("You: ")
    elapsed = time.time() - start_time

    # check if the user took too long to answer
    if elapsed > time_limit:
        evasive += 1
        return choose_random_response(response_times_up)

    # check if the user's answer contains any of the keywords, then determine if it's cooperative, evasive, or uncooperative
    for keyword in keywords:
        if keyword.lower() in user_input.lower():
            # check if the user is giving an explanation by looking for certain words that indicate an explanation
            explanation = any(word in user_input.lower() 
                              for word in keywords_explanation)

            # if the user uses words that indicate giving an explanation, consider it cooperative
            if explanation and len(user_input.split()) > 5:
                cooperative += 1
                return choose_random_response(response_positive)
            # if the user uses words that indicate giving an explanation but their answer is short, consider it evasive
            elif explanation:
                cooperative += 1
                return choose_random_response(response_evasive)
            # if the user uses any of the wanted answer keywords but doesn't give an explanation, consider it evasive
            else:
                evasive += 1
                return choose_random_response(response_evasive)
    
    # check if the user's answer contains any of the hostile or unhelpful keywords
    if any(hostile in user_input.lower() for hostile in hostile_answers):
        uncooperative += 1
        return choose_random_response(response_passive_aggressive)
    elif any(evasive in user_input.lower() for evasive in evasive_answers):
        evasive += 1
        return choose_random_response(response_evasive)
    else:
        return choose_random_response(response_nuetral)

# function to choose a random response from a given response type
def choose_random_response(response_type):
    return "Officer: " + random.choice(response_type)

def evaluate_cooperation():
    global cooperative, uncooperative, evasive

    if cooperative > uncooperative and cooperative > evasive:
        return "Officer: Thank you for your cooperation. This will be taken into account."
    elif uncooperative > cooperative and uncooperative > evasive:
        return "Officer: Your lack of cooperation is noted. This may have consequences."
    elif evasive > cooperative and evasive > uncooperative:
        return "Officer: Your evasiveness is noted. This may have consequences."
    else:
        return "Officer: Your responses are inconclusive. We will continue to evaluate your cooperation."

# main function to run the game
def main():
    print("Officer: Sit down.")
    time.sleep(2)

    print("Officer: Let us get started.")
    time.sleep(2)
    print()

    # ask where
    print(ask_adaptive_question(questions_where, keywords_where))
    time.sleep(2)
    print()

    # ask when
    print(ask_adaptive_question(questions_when, keywords_when))
    time.sleep(2)
    print()

    # ask why
    print(ask_adaptive_question(questions_why, keywords_why))
    time.sleep(2)
    print()

    # print vague response to the user's previous answers rasing questions (even if it doesn't)
    print("Officer: " + random.choice(response_vague))
    time.sleep(2)

    # pick a random question to reask
    random_question = random.choice([[questions_why, keywords_why], [questions_where, keywords_where], [questions_when, keywords_when]])
    print(ask_adaptive_question(random_question[0], random_question[1]))
    time.sleep(2)
    print()

    # print a message that the user's statements are inconsistent
    print("Officer: Your statements are inconsistent.")
    print("Officer: This will be noted.")
    time.sleep(2)
    print()

    # add a tense pause
    print("Officer: ...")
    time.sleep(4)
    print()

    # ask final question
    print(ask_adaptive_question(questions_final, keywords_explanation))
    time.sleep(2)
    print()

    # evaluate the user's cooperation level and print a message
    print("Officer: Your responses have been recorded. This concludes the interview.")
    time.sleep(2)
    print(evaluate_cooperation())
    time.sleep(2)

if __name__ == "__main__":
    main()