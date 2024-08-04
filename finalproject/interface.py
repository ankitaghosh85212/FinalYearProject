import tkinter as tk
from tkinter import Frame, Label, Entry, Button, Toplevel, messagebox
from tkinter import ttk
import re
import ast
from gad7 import question_data1
from phq import question_data3
from tkinter import *
import joblib
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF

try:
    modelAnxiety = joblib.load("modelAnxiety.pkl")
    modelDepression = joblib.load("modelDepression.pkl")
except Exception as e:
    print(f"Error loading models: {e}")
def read_user_data(file_path):
    with open(file_path, 'r') as file:
        user_data = {}
        for line in file:
            user_data.update(ast.literal_eval(line.strip()))
    return user_data

# Load user data from datasheet2.txt
user_data = read_user_data('datasheet2.txt')    
def store_score(test_type, score):
    with open("scores.txt", "a") as file:
        file.write(f"Username: {current_user}, Test: {test_type}, Score: {score}\n")
def destroywindow(window):
    window.destroy()    
def plot_graphs(user_score, average_score, title, xlabel, ylabel, comparison_label):
    labels = ['User Score', 'Average Score']
    scores = [user_score, average_score]
    x = np.arange(len(labels))
    width = 0.2
    colors = ['blue', 'green']  # Colors for User Score and Average Score    
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, scores, width, label=comparison_label, color=colors)    
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()    
    for rect in rects1:
        height = rect.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')    
    plt.savefig("result.png")    
def show_comparison_graphs(score,test_type):
    if test_type == 'Anxiety':
        average_score = 6.810983397190293  # Average score for normal people calculated from the dataset
        title = 'GAD-7 Anxiety Score Comparison'
        xlabel = 'Type'
        ylabel = 'Score'
        comparison_label = 'Anxiety Level'
    else:
        average_score = 7.123882503192848  # Average score for normal people calculated from the dataset
        title = 'PHQ-9 Depression Score Comparison'
        xlabel = 'Type'
        ylabel = 'Score'
        comparison_label = 'Depression Level'    
    plot_graphs(score, average_score, title, xlabel, ylabel, comparison_label)    
def generate_pdf_reportA(user_info, score, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # Add user information
    pdf.cell(200, 10, txt="User Information", ln=True, align="C")
    pdf.ln(10)
    for key, value in user_info.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True, align="L")
    pdf.ln(10)
    # Add score and analysis title
    pdf.cell(200, 10, txt="GAD-7 Anxiety Score Analysis", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Anxiety Score: {score}", ln=True, align="L")
    pdf.ln(10)
    # Replace bullet points and add content
    content = content.replace("•", "-")
    pdf.multi_cell(0, 10, txt=content.encode('latin-1', 'replace').decode('latin-1'))
    # Add comparison graph
    pdf.ln(10)
    pdf.image('result.png', x=10, y=None, w=190)
    # Save the PDF
    pdf.output("result_Anxiety.pdf")
    messagebox.showinfo("Report Saved", "The report has been successfully generated and saved as 'result_Anxiety.pdf'.")
    
def ScoreAnalysisA(score,window):
    destroywindow(window)
    username=user.get()
    with open("datasheet2.txt", "r") as file:
            d = file.read()
            r = ast.literal_eval(d)
    Age=r[username]['age']
    Gender=r[username]['gender']
    user_info = {
        "Name": username,  # Replace with actual user information
        "Age": Age,
        "Gender": Gender
    }
    Ascore = score
    show_comparison_graphs(Ascore, 'Anxiety')
    def anxietyscore(Ascore):

        Ascorescreen = Toplevel(root)
        Ascorescreen.title("Analysis")
        Ascorescreen.geometry("925x600+300+200")
        Ascorescreen.resizable(True, True)

        header_font = ("Arial", 16, "bold")
        body_font = ("Arial", 12)
        bg_color = "#f0f0f0"
        header_color = "#007acc"
        text_color = "#333333"

        header_frame = Frame(Ascorescreen, bg=header_color)
        header_frame.pack(fill='x')
        Label(header_frame, text="GAD-7 Anxiety Score Analysis", bg=header_color, fg="white", font=header_font).pack(pady=10)
        
        frame = Frame(Ascorescreen, bg='white')
        frame.pack(padx=20, pady=20, fill='both', expand=True)
        
        footer_frame = Frame(Ascorescreen, bg=header_color)
        footer_frame.pack(fill='x', side='bottom')
        Label(footer_frame, text="Consult a healthcare professional for personalized advice.", bg=header_color, fg="white", font=("Arial", 10)).pack(pady=5)
        
        def create_content(text):
            Label(frame, text=text, bg=bg_color, font=("Arial", 12), wraplength=800, justify='left').pack(anchor="w", pady=5)

        if 0 <= Ascore <= 4:
            content = (
                "There are many ways to treat minimal anxiety without medication, including:\n"
                "• Mindfulness: Focus on the present moment, such as with mindful meditation.\n"
                "• Exercise: Regular exercise can help reduce stress and anxiety symptoms.\n"
                "• Self-care: Try yoga, meditation, aromatherapy, massage, reflexology, herbal treatments, Bach flower remedies, or hypnotherapy.\n"
                "• Stress management: Learn ways to manage stress, such as through meditation.\n"
                "• Support groups: Share your experiences and coping strategies with others who have anxiety disorders.\n"
                "• Education: Learn about your specific type of anxiety disorder so you feel more in control.\n"
                "• Avoid triggers: Manage triggers that can lead to stress, such as work pressures and deadlines, and take time off from obligations.\n"
                "• Relaxation techniques: Try deep-breathing exercises, long baths, yoga, and resting in the dark.\n"
                "• Maintain a support network: Talk with family, friends, or a support group, and avoid storing up anxious feelings.\n"
                "• Limit screen time: Using smartphones, computers, and tablets too often can increase stress levels and negatively affect sleep."
            )
        elif 4 < Ascore <= 9:
            content = (
                "Mild anxiety is characterized by constant worries, irritability, and feeling nervous, nauseated, shaky, or sweaty. It can be managed without additional techniques. Here are some suggestions for treating mild anxiety:\n"
                "• Relaxation techniques: Try meditation, visualization, or yoga. You can also try the 333 rule, which involves naming three things you can see, three you can hear, and moving three different body parts.\n"
                "• Exercise: Regular exercise can help reduce stress and anxiety symptoms.\n"
                "• Healthy eating: Focus on eating vegetables, fruits, whole grains, and fish.\n"
                "• Avoid substances: Avoid alcohol, recreational drugs, nicotine, and caffeine, which can worsen anxiety.\n"
                "• Get enough sleep: Make sure you're getting enough sleep to feel rested.\n"
                "• Do what you enjoy: Take a bath, get a massage, fish, garden, read, nap, or spend time with family and friends."
            )
        elif 9 < Ascore <= 14:
            content = (
                "Here are some ways to treat moderate anxiety:\n"
                "• Lifestyle changes\n"
                "• Exercise: Being physically active can reduce stress and improve your mood.\n"
                "• Sleep: Make sure you're getting enough sleep to feel rested. If you're not sleeping well, talk to your healthcare provider.\n"
                "• Diet\n"
                "• Relaxation techniques\n"
                "• Try meditation, yoga, or visualization techniques. You can also try the 333 rule, which involves naming three things you can see, three you can hear, and moving three different body parts.\n"
                "• Other techniques:\n"
                "• You can also try learning about anxiety, mindfulness, correct breathing techniques, structured problem solving, and building self-esteem.\n"
                "• Support\n"
                "• Join a support group, either in-person or online, to share your experiences and coping strategies with others. You can also help friends and loved ones understand your disorder so they can support you.\n"
                "• Therapy\n"
                "• Consider cognitive therapy or exposure therapy. You can also take medications as directed and keep therapy appointments."
            )
        else:
            content = (
                "Here are some ways to treat severe anxiety:\n"
                "• Cognitive behavioral therapy (CBT)\n"
                "• CBT is a type of psychotherapy that helps you learn to face stressful situations and reduce anxiety.\n"
                "• Medication\n"
                "• Selective serotonin reuptake inhibitors (SSRIs) and serotonin-norepinephrine reuptake inhibitors (SNRIs) are first-line drugs for treating anxiety. Benzodiazepines are also sometimes used, but they aren't recommended for routine use. Only recommended when prescribed by your health provider.\n"
                "• Relaxation techniques\n"
                "• Visualization, meditation, yoga, and breathing exercises can help ease anxiety.\n"
                "• Lifestyle changes\n"
                "• Avoid or cut back on caffeine and nicotine, which can worsen anxiety. Eating healthy foods, like fruits, vegetables, whole grains, and fish, may also help. Getting enough sleep and exercising can also help reduce stress and improve your overall well-being.\n"
                "• Other techniques:\n"
                "• Art therapy, support groups, and structured problem solving can also be helpful.\n"
                "• Support\n"
                "• Join a support group, either in-person or online, to share your experiences and coping strategies with others. You can also help friends and loved ones understand your disorder so they can support you."
            )
        create_content(content)
        generate_pdf_reportA(user_info, Ascore, content)
    anxietyscore(Ascore)
    
def generate_pdf_reportD(user_info, score, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)    
    # Add user information
    pdf.cell(200, 10, txt="User Information", ln=True, align="C")
    pdf.ln(10)
    for key, value in user_info.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True, align="L")
    pdf.ln(10)    
    # Add score and analysis title
    pdf.cell(200, 10, txt="PHQ-9 Depression Score Analysis", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Depression Score: {score}", ln=True, align="L")
    pdf.ln(10)    
    # Replace bullet points and add content
    content = content.replace("•", "-")
    pdf.multi_cell(0, 10, txt=content.encode('latin-1', 'replace').decode('latin-1'))    
    # Add space for the image
    pdf.ln(10)    
    # Check if the image file exists before adding it
    try:
        pdf.image('result.png', x=10, y=None, w=190)
    except RuntimeError as e:
        messagebox.showerror("Image Error", f"An error occurred while adding the image: {e}")    
    # Save the PDF
    pdf.output("result_Depression.pdf")
    messagebox.showinfo("Report Saved", "The report has been successfully generated and saved as 'result_Depression.pdf'.")



def ScoreAnalysisD(score,window):
    destroywindow(window)
    username=user.get()
    with open("datasheet2.txt", "r") as file:
            d = file.read()
            r = ast.literal_eval(d)
    Age=r[username]['age']
    Gender=r[username]['gender']
    user_info = {
        "Name": username,  # Replace with actual user information
        "Age": Age,
        "Gender": Gender
    }
    Dscore=score
    show_comparison_graphs(Dscore,'Depression')
    def depressionscore(Dscore):
        Dscorescreen = Toplevel(root)
        Dscorescreen.title("Analysis")
        Dscorescreen.geometry("925x600+300+200")
        Dscorescreen.resizable(True, True)
        header_font = ("Arial", 16, "bold")
        body_font = ("Arial", 12)
        bg_color = "#f0f0f0"
        header_color = "#007acc"
        text_color = "#333333"
        header_frame = Frame(Dscorescreen, bg=header_color)
        header_frame.pack(fill='x')
        Label(header_frame, text="PHQ-9 Depression Score Analysis", bg=header_color, fg="white", font=header_font).pack(pady=10)
        footer_frame = Frame(Dscorescreen, bg=header_color)
        footer_frame.pack(fill='x', side='bottom')
        Label(footer_frame, text="Consult a healthcare professional for personalized advice.", bg=header_color, fg="white", font=("Arial", 10)).pack(pady=5)
        frame = Frame(Dscorescreen, bg='white')
        frame.pack(padx=20, pady=20, fill='both', expand=True)
        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        if Dscore >= 0 and Dscore <= 4:
            advice_text = ("There are many ways to treat minimal depression:\n"
                           "Lifestyle changes:\n"
                           "1. Exercise: Activities like jogging, swimming, cycling, hiking, or Nordic walking can help relieve or prevent depression.\n"
                           "2. Sleep: Getting enough quality sleep is important for your mental and physical health. If you're having trouble sleeping, talk to your doctor.\n"
                           "3. Diet: Eating healthy foods can help improve your mood. Avoid alcohol and recreational drugs as they can worsen depression.\n"
                           "4. Spend time with others: Spending time with people you care about can help improve your mood.\n"
                           "5. Psychological therapy: Psychological therapy can be an important treatment for depression.\n")
        elif Dscore >= 5 and Dscore <= 9:
            advice_text = ("Here are some treatments that may help with mild depression:\n"
                           "1. Exercise: Physical activity like jogging, swimming, cycling, or hiking can help relieve or prevent depression.\n"
                           "2. Sleep: Getting enough quality sleep is important for both your physical and mental well-being.\n"
                           "3. Diet: Eating a healthy diet can help improve depression symptoms.\n"
                           "4. Avoid substances: Alcohol and recreational drugs can make depression harder to treat, so it's best to avoid them.\n"
                           "5. Spend time with others: Spending time with people you care about can help.\n"
                           "6. Relaxation techniques: Some evidence suggests that relaxation techniques and yoga can help relieve mild to moderate depression.\n"
                           "7. Guided self-help: Your doctor may suggest trying guided self-help.\n"
                           "8. Talking therapies: If your depression isn't improving, a talking therapy may be helpful.\n")
        elif Dscore >= 10 and Dscore <= 14:
            advice_text = ("Here are some ways to treat moderate depression:\n"
                           "1. Psychological treatments: Talking therapies like cognitive behavioral therapy (CBT), interpersonal therapy (IPT), and mindfulness-based cognitive therapy (MBCT) can help.\n"
                           "2. Lifestyle changes:\n"
                           "   - Exercise: Regular exercise can lower stress, relax you, and help lessen symptoms of depression.\n"
                           "   - Sleep: Getting quality sleep is important for both your physical and mental well-being.\n"
                           "   - Diet: Eat a healthy diet and avoid too much sugar, which can trigger emotional highs and lows.\n"
                           "   - Avoid substances: Alcohol and recreational drugs can worsen depression symptoms.\n"
                           "   - Spend time with others: Spend time with people you care about.\n"
                           "3. Other non-drug approaches: Relaxation techniques, yoga, meditation, massage therapy, and music therapy.\n")
        elif Dscore >= 15 and Dscore <= 19:
            advice_text = ("There are several treatments for moderate depression, including:\n"
                           "1. Lifestyle changes:\n"
                           "   - Exercise: Regular exercise such as jogging, cycling, swimming, or hiking can help relieve or prevent depression.\n"
                           "   - Sleep: Getting enough quality sleep is important for both physical and mental health.\n"
                           "   - Diet: Eating a healthy diet and avoiding alcohol can help improve depression symptoms.\n"
                           "   - Social support: Spending time with people you care about can help.\n"
                           "2. Psychological treatments: Talking therapies like CBT, IPT, behavior therapy, and MBCT.\n")
        else:
            advice_text = ("For severe depression, a combination of psychotherapy and antidepressants is often recommended. Antidepressants can take 4 to 8 weeks to have a full effect. Psychotherapy can help you change your thinking patterns and coping skills. Some types of psychotherapy include:\n"
                           "1. Cognitive behavioral therapy (CBT)\n"
                           "2. Interpersonal therapy (IPT)\n"
                           "3. Mindfulness-based cognitive therapy (MBCT)\n")        
        Label(frame, text=advice_text, bg=bg_color, fg=text_color, font=body_font, wraplength=800, justify=tk.LEFT).pack(anchor="w", pady=10)

        generate_pdf_reportD(user_info, Dscore, advice_text)
    depressionscore(Dscore)


def make_prediction_depression(score):
    try:
        username=user.get()
        with open("datasheet2.txt", "r") as file:
            d = file.read()
            r = ast.literal_eval(d)
        Age=r[username]['age']
        Gender=r[username]['gender']
        age_mapping = {
                 '18':1,
                 '19':1,
                 '20':1,
                 '21':2,
                 '22':2,
                 '23':2,
                 '24':2,
                 '25':2,
                 '26':3,
                 '27':3,
                 '28':3,
                 '29':3,
                 '30':3,
                 '31':3,

            }
        Age_mapped = age_mapping.get(str(Age), 0)
        gender_mapping={
              'Male': True,
              'Female':False,
         }
        mapped_gender = gender_mapping.get(str(Gender), None)
        predictionD = modelDepression.predict([[score,Age_mapped,mapped_gender]])
        predictScore=predictionD[0]
        if predictScore==0:
            messagebox.showinfo("prediction",f" your PHQ-9 score is:{score} your depression level is Minimal ")
        elif predictScore==1:
            messagebox.showinfo("prediction", f"your PHQ-9 score is:{score} your depression level is Mild")
        elif predictScore==2:
            messagebox.showinfo("prediction", f"your PHQ-9 score is:{score} your depression level is Moderate")
        elif predictScore==3:
            messagebox.showinfo("prediction", f"your PHQ-9 score is:{score} your depression level is Moderately severe")
        else:
            messagebox.showinfo("prediction", f"your PHQ-9 score is:{score} your depression level is Severe")
    except Exception as e:
        messagebox.showerror("Error", f"Error making depression prediction: {e}")
        return None
def make_prediction_anxiety(score):
    try:
        username=user.get()
        with open("datasheet2.txt", "r") as file:
            d = file.read()
            r = ast.literal_eval(d)
        Age=r[username]['age']
        Gender=r[username]['gender']
        age_mapping = {
                  '18':1,
                  '19':1,
                  '20':1,
                  '21':2,
                  '22':2,
                  '23':2,
                  '24':2,
                  '25':2,
                  '26':3,
                  '27':3,
                  '28':3,
                  '29':3,
                  '30':3,
                  '31':3,
            }
        Age_mapped = age_mapping.get(str(Age), 0)
        gender_mapping={
              'Male': True,
              'Female':False,
         }
        mapped_gender = gender_mapping.get(str(Gender), None)
        predictionA = modelAnxiety.predict([[score,Age_mapped,mapped_gender]])
        predictScoreA = predictionA[0]
        if predictScoreA == 0:
            messagebox.showinfo("prediction", f" your GAD-7 score is:{score} your anxiety level is Minimal ")
        elif predictScoreA == 1:
            messagebox.showinfo("prediction", f"your GAD-7 score is:{score} your anxiety level is Mild")
        elif predictScoreA == 2:
            messagebox.showinfo("prediction", f"your GAD-7 score is:{score} your anxiety level is Moderate")
        else:
            messagebox.showinfo("prediction", f"your GAD-7 score is:{score} your anxiety level is Severe")
    except Exception as e:
        messagebox.showerror("Error", f"Error making anxiety prediction: {e}")
        return None



def GAD7Q():
    ContWindow.destroy()
    global score, current_question,Q
    score = 0
    current_question = 0
    QuestionWindowGAD = Toplevel(root)
    QuestionWindowGAD.title("GAD7")
    QuestionWindowGAD.geometry("925x600+300+200")
    QuestionWindowGAD.resizable(True, True)
    QuestionWindowGAD.configure(bg="#87CEEB")

    def check_answer(choice):
        global score
        question = question_data1[current_question]
        selected_choice = choice_buttons[choice].cget("text")
        selected_index = question["choices"].index(selected_choice)
        score += question["scores"][selected_index]
        score_label.config(text="Score: {}".format(score))
        for button in choice_buttons:
            button.config(state="disabled",background="light pink",fg="black",font=("Arial Black",11))
        next_button.config(state="normal")

    def Next_Question():
        global current_question
        current_question += 1
        if current_question < len(question_data1):
            show_question()
        else:
            predictionA = make_prediction_anxiety(score)
            store_score("GAD-7",score)
            QuestionWindowGAD.destroy()
            
    b3 = Button(frame, fg="white", bg="#00008B", text="Score Analysis", width=30, height=2,command=lambda: ScoreAnalysisA(score,QuestionWindowGAD))
    b3.pack(anchor="w", pady=(10, 25))
    def show_question():
        question = question_data1[current_question]
        qs_label.config(text=question["question"])
        choices = question["choices"]
        for i in range(4):
            choice_buttons[i].config(text=choices[i], state="normal",bg="#00008B",fg="white",font=("Arial Black",11))
        next_button.config(state="disabled")    

    qs_label = Label(QuestionWindowGAD, anchor="center", wraplength=500, font=("Helvetica", 16, "bold"), background="#87CEEB")
    qs_label.pack(pady=10)

    choice_buttons = []
    for i in range(4):
        button = Button(QuestionWindowGAD,width=20,height=1, command=lambda i=i: check_answer(i))
        button.pack(pady=5)
        choice_buttons.append(button)

    score_label = Label(QuestionWindowGAD, text="Score: 0", anchor="e",fg="black",font=("Helvetica",12,"bold"), background="#87CEEB")
    score_label.pack(pady=5)

    next_button = Button(QuestionWindowGAD, text="NEXT", command=Next_Question, state="disabled",bg="plum1",fg="black",font=("Arial",12,"bold"))
    next_button.pack(pady=10)

    show_question()
    
def PHQQ():
    ContWindow.destroy()

    
    global score, current_question
    score = 0
    current_question = 0
    QuestionWindow = Toplevel(root)
    QuestionWindow.title("PHQ9")
    QuestionWindow.geometry("925x600+300+200")
    QuestionWindow.resizable(True, True)
    QuestionWindow.configure(bg="#87CEEB")
    

    def check_answer(choice):
        global score
        question = question_data3[current_question]
        selected_choice = choice_buttons[choice].cget("text")
        selected_index = question["choices"].index(selected_choice)
        score += question["scores"][selected_index]
        score_label.config(text="Score : {}".format(score))
        for button in choice_buttons:
            button.config(state="disabled",background="light pink",fg="black",font=("Arial Black",11))
        next_button.config(state="normal")

    def Next_Question():
        global current_question
        current_question += 1
        if current_question < len(question_data3):
            show_question()
        else:
            predictionD = make_prediction_depression(score)
            store_score("PHQ-9",score)
            QuestionWindow.destroy()
            
    b3 = Button(frame, fg="white",  bg="#00008B", text="Score Analysis", width=30, height=2,command=lambda: ScoreAnalysisD(score,QuestionWindow))
    b3.pack(anchor="w", pady=(10, 25))

    def show_question():
        question = question_data3[current_question]
        qs_label.config(text=question["question"])
        choices = question["choices"]
        for i in range(4):
            choice_buttons[i].config(text=choices[i], state="normal",bg="#00008B",fg="white",font=("Arial Black",11))
        next_button.config(state="disabled")    

    qs_label = Label(QuestionWindow, anchor="center", wraplength=500,font=("Helvetica", 16, "bold"),background="#87CEEB")
    qs_label.pack(pady=10)

    choice_buttons = []
    for i in range(4):
        button = Button(QuestionWindow,width=20,height=1, command=lambda i=i: check_answer(i))
        button.pack(pady=5)
        choice_buttons.append(button)

    score_label = Label(QuestionWindow, text="Score:", anchor="ne",fg="black",font=("Helvetica",12,"bold"), background="#87CEEB")
    score_label.pack(pady=5)

    next_button = Button(QuestionWindow, text="NEXT", command=Next_Question, state="disabled",bg="plum1",fg="black",font=("Arial",12,"bold"))
    next_button.pack(pady=10)

    show_question() 
def Cont_Window():
    global ContWindow
    ContWindow = Toplevel(root)
    ContWindow.title("Test Options")
    ContWindow.geometry("925x600+300+200")
    ContWindow.resizable(True, True)
    ContWindow.configure(bg="#87CEEB")

    Label(ContWindow, text="Choose the test you want to give!", background='#87CEEB', font=("Arial", 20, "bold")).pack(side="top", pady=20)

    frame = Frame(ContWindow, bg='#87CEEB')
    frame.pack(side=tk.LEFT, anchor=tk.NW, padx=40, pady=20)

    phq9_frame = Frame(frame, bg='#E0FFFF', bd=2, relief='groove', padx=10, pady=10)
    phq9_frame.pack(anchor="w", pady=(10, 20), fill='x')

    Label(phq9_frame, text="PHQ-9 (Patient Health Questionnaire-9)", bg='#E0FFFF', font=("Arial", 16, "bold")).pack(anchor="w", pady=(5, 5))
    Label(phq9_frame, text="The PHQ-9 is a multipurpose instrument for screening, diagnosing, monitoring, and measuring the severity of depression.",
          bg='#E0FFFF', font=("Arial", 12), wraplength=700, justify=tk.LEFT).pack(anchor="w", pady=5)
    b1 = Button(phq9_frame, fg="white", bg="#4682B4", text="Take PHQ-9 Test", width=30, height=2, command=PHQQ)
    b1.pack(anchor="w", pady=(10, 5))

    gad7_frame = Frame(frame, bg='#E6E6FA', bd=2, relief='groove', padx=10, pady=10)
    gad7_frame.pack(anchor="w", pady=(10, 20), fill='x')

    Label(gad7_frame, text="GAD-7 (Generalized Anxiety Disorder-7)", bg='#E6E6FA', font=("Arial", 16, "bold")).pack(anchor="w", pady=(5, 5))
    Label(gad7_frame, text="The GAD-7 is a screening tool that measures the severity of generalized anxiety disorder.",
          bg='#E6E6FA', font=("Arial", 12), wraplength=700, justify=tk.LEFT).pack(anchor="w", pady=5)
    b2 = Button(gad7_frame, fg="white", bg="#4682B4", text="Take GAD-7 Test", width=30, height=2, command=GAD7Q)
    b2.pack(anchor="w", pady=(10, 5))
    
    
    
   

    
def signin():
    global current_user
    username = user.get()  
    current_user=username   
    password = pas.get()
    try:
        with open("datasheet2.txt", "r") as file:
            d = file.read()
            r = ast.literal_eval(d)
    except Exception as e:
        messagebox.showerror("Error", f"Error reading user data: {e}")
        return

    if username in r.keys() and password == r[username]['password']:
       messagebox.showinfo("successfull",'login successfull')
       Cont_Window()
       
    else:
        messagebox.showerror("Invalid", "Invalid username or password")
       




def signup_command():
    window = Toplevel(root)
    window.title("SignUp")
    window.geometry("925x600+300+200")
    window.configure(bg="#87CEEB")

    def is_strong_password(password):
        return (len(password) >= 6 and
                re.search(r'[A-Z]', password) and
                re.search(r'[a-z]', password) and
                re.search(r'[0-9]', password) and
                re.search(r'[\W_]', password))

    def show_password_strength(event):
        password = pas.get()
        if len(password) < 6:
            strength_label.config(text="Password too short", fg="red")
        elif is_strong_password(password):
            strength_label.config(text="Strong password", fg="green")
        else:
            strength_label.config(text="Weak password", fg="red")

    def signup():
        username = user.get()
        password = pas.get()
        confirm_password = confirm_pass.get()
        age_value = age.get()
        gender_value = gender.get()

        if password != confirm_password:
            messagebox.showerror("Invalid", "Passwords do not match")
            return

        if not is_strong_password(password):
            messagebox.showerror("Invalid", "Password must be at least 6 characters long and include upper and lower case letters, numbers, and special characters.")
            return

        try:
            with open("datasheet2.txt", "r") as file:
                d = file.read()
                r = ast.literal_eval(d) if d else {}
                r[username] = {'password': password, 'age': age_value, 'gender': gender_value}
        except Exception as e:
            r = {username: {'password': password, 'age': age_value, 'gender': gender_value}}

        with open("datasheet2.txt", "w") as file:
            file.write(str(r))

        messagebox.showinfo("Sign Up", "SignUp successful")
        sign()

    def sign():
        window.destroy()

    # Load image for the signup window
    imagepath = r"C:\Users\Ankita\Desktop\finalproject\mh2.png"
    img = tk.PhotoImage(file=imagepath)
    Label(window, image=img, border=0, bg='#87CEEB').place(x=50, y=90)

    frame = Frame(window, width=600, height=500, bg='#87CEEB')
    frame.place(x=480, y=50)

    heading = Label(frame, text="Sign up", fg="#00008B", bg="#87CEEB", font=("Microsoft YaHei UI Light", 23, "bold"))
    heading.place(x=100, y=5)

    def on_enter(e, widget, placeholder):
        if widget.get() == placeholder:
            widget.delete(0, 'end')
            widget.config(show='')

    def on_leave(e, widget, placeholder):
        if widget.get() == '':
            widget.insert(0, placeholder)
            if 'password' in placeholder:
                widget.config(show='*')

    def on_enter1(event, widget, placeholder):
        if widget.get() == placeholder:
            widget.delete(0, "end")
            widget.config(fg='black')

    def on_leave1(event, widget, placeholder):
        if widget.get() == "":
            widget.insert(0, placeholder)
            widget.config(fg='grey')

    user = Entry(frame, width=25, fg='black', border=0, bg="#87CEEB", font=("Microsoft YaHei UI Light", 11,"bold"))
    user.place(x=30, y=80)
    user.insert(0, "username")
    user.bind("<FocusIn>", lambda e: on_enter(e, user, "username"))
    user.bind("<FocusOut>", lambda e: on_leave(e, user, "username"))
    Frame(frame, width=295, height=2, bg="black").place(x=25, y=107)

    pas = Entry(frame, width=25, fg="black", border=0, bg="#87CEEB", font=("Microsoft YaHei UI Light", 11,"bold"))
    pas.place(x=30, y=150)
    pas.insert(0, "password")
    pas.bind("<FocusIn>", lambda e: on_enter(e, pas, "password"))
    pas.bind("<FocusOut>", lambda e: on_leave(e, pas, "password"))
    pas.bind("<KeyRelease>", show_password_strength)
    Frame(frame, width=295, height=2, bg="black").place(x=25, y=177)

    confirm_pass = Entry(frame, width=25, fg='black', border=0, bg="#87CEEB", font=("Microsoft YaHei UI Light", 11,"bold"))
    confirm_pass.place(x=30, y=220)
    confirm_pass.insert(0, "confirm password")
    confirm_pass.bind("<FocusIn>", lambda e: on_enter(e, confirm_pass, "confirm password"))
    confirm_pass.bind("<FocusOut>", lambda e: on_leave(e, confirm_pass, "confirm password"))
    Frame(frame, width=295, height=2, bg="black").place(x=25, y=247)
   
    age_label = Label(frame, text="Age:", bg="#87CEEB", font=("Microsoft YaHei UI Light", 11,"bold"))
    age_label.place(x=30, y=260)
    age_options = [str(i) for i in range(18, 32)]
    age = ttk.Combobox(frame, values=age_options, width=23, font=("Microsoft YaHei UI Light", 11,"bold"))
    age.place(x=30, y=290)
    age.set("Age")
    age.config(foreground='black')
    age.bind("<FocusIn>", lambda e: on_enter1(e, age, "Age"))
    age.bind("<FocusOut>", lambda e: on_leave1(e, age, "Age"))

    gender_label = Label(frame, text="Gender:", bg="#87CEEB", font=("Microsoft YaHei UI Light", 11,"bold"))
    gender_label.place(x=30, y=330)
    gender = ttk.Combobox(frame, width=22, font=("Microsoft YaHei UI Light", 11,"bold"))
    gender['values'] = ("Male", "Female")
    gender.place(x=30, y=360)
    gender.set("Select Gender")
    underline = Frame(frame, width=295, height=2, bg="black")
    underline.place(x=25, y=387)
    separator = Frame(frame, width=295, height=2, bg="black")
    separator.place(x=25, y=317)

    strength_label = Label(frame, text="", fg="red", bg="#87CEEB", font=("Microsoft YaHei UI Light", 9,"bold"))
    strength_label.place(x=30, y=190)

    Button(frame, width=39, pady=7, text="Sign up", bg="#00008B", fg="white", border=0, command=signup).place(x=35, y=400)
    label = Label(frame, text="I have an account", fg="black", bg="#87CEEB", font=("Microsoft YaHei UI Light", 9,"bold"))
    label.place(x=70, y=457)
    signin = Button(frame, width=6, text="Sign in", border=0, bg="#87CEEB", cursor="hand2", fg="#00008B", command=sign)
    signin.place(x=200, y=457)

    window.mainloop()

root = tk.Tk()
root.title("Login")
root.configure(bg="#87CEEB")
root.geometry("925x600+200+300")  
root.resizable(True, True)
imagepath = "mh2.png"  # Ensure the path to the image is correct
img = tk.PhotoImage(file=imagepath) 
Label(root, image=img, bg="#87CEEB").place(x=50, y=50)
frame = Frame(root, width=350, height=350, bg="#87CEEB")
frame.place(x=500, y=70)
heading = Label(frame, text="Sign In", fg="#00008B", bg="#87CEEB", font=("Microsoft YaHei UI Light", 23, "bold"))
heading.place(x=100, y=5)

def on_enter(e):
    user.delete(0, 'end')

def on_leave(e):
    name = user.get()
    if name == '':
        user.insert(0, 'username')

user = Entry(frame, width=25, fg="black", border=0, bg="#87CEEB", font=("Microsoft YaHei UI Light", 11,"bold"))
user.place(x=30, y=80)
user.insert(0, "username")
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)
Frame(frame, width=210, height=2, bg="black").place(x=25, y=107)

def on_enter(e):
    pas.delete(0, 'end')
    pas.config(show="*")

def on_leave(e):
    name = pas.get()
    if name == '':
        pas.insert(0, "password")
        pas.config(show="")

pas = Entry(frame, width=25, fg="black", border=0, bg="#87CEEB", font=("Microsoft YaHei UI Light", 11,"bold"))
pas.place(x=30, y=150)
pas.insert(0, "password")
pas.bind("<FocusIn>", on_enter)
pas.bind('<FocusOut>', on_leave)
Frame(frame, width=210, height=2, bg="black").place(x=25, y=177)



Button(frame, width=40, pady=10, text="Sign-In", bg="#00008B", fg="white", border=0,command=signin).place(x=27, y=200)
label = Label(frame, text="Don't have an account?", fg='black', bg='#87CEEB', font=("Microsoft YaHei UI Light", 9,"bold"))
label.place(x=65, y=270)
sign_up = Button(frame, width=6, text="Sign up", border=0, bg='#87CEEB', cursor='hand2', fg='#00008B',command=signup_command)
sign_up.place(x=225, y=270)

root.mainloop()