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

questions_

# array of positive and negative affirmative keywords for questions
positive_answers = ["yes", "yeah", "yep", "sure", "correct", "right"]
negative_answers = ["no", "nope", "nah", "not", "incorrect", "wrong"]

# array of hostile/unhelpful keywords for questions
hostile_answers = ["don't have to", "none of your business", "refuse to answer", "not answering", "not telling you", "not saying", "not going to say", "not going to tell you"]
unhelpful_answers = ["have rights", "lawyer", "no comment", "don't know", "dont know", "not sure", "can't remember", "cant remember", "no idea", "can't recall", "cant recall", "not certain", "not positive", "not 100% sure", "no thanks", "not answering", "not telling you", "not saying", "not going to say", "not going to tell you"]

# array of types of responses for each question
response_positive = ["That sounds good.", "I appreciate your cooperation.", "Thank you for your honesty.", "I see. That makes sense."]
response_evasive = ["I see.", "Okay.", "Alright.", "Hmm.", "Interesting."]
response_nuetral = ["Thank you for your answer.", "I understand.", "Noted."]
response_passive_aggressive = ["Are you sure about that?", "That doesn't sound right.", "I find that hard to believe.", "Is that so?"]
response_times_up = ["Time's up.", "You have run out of time.", "You took too long to answer.", "Your time is up."]

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
                              for word in ["because", "since", "went", "was"])

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
    elif any(unhelpful in user_input.lower() for unhelpful in unhelpful_answers):
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

    print(ask_adaptive_question(questions_where, keywords_where))
    time.sleep(2)
    print()

    print(ask_adaptive_question(questions_when, keywords_when))
    time.sleep(2)
    print()

    print(ask_adaptive_question(questions_why, keywords_why))
    time.sleep(2)
    print()

    # add more questions as needed
    time.sleep(2)
    print()

    print(evaluate_cooperation())
    time.sleep(2)

if __name__ == "__main__":
    main()