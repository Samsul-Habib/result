from flask import Flask, request, render_template
app = Flask(__name__)
student_id,course_id,marks=[],[],[]
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend (non-interactive mode) before importing pyplot
import matplotlib.pyplot as plt
import os
# Open the CSV file
with open('data.csv', 'r') as file:
    # Skip the header row if it exists
    next(file)
    # Iterate over each line in the file
    for line in file:
        # Split the line into columns based on comma
        columns = line.strip().split(',')
        # Extract data from each column and append to respective lists
        student_id.append(int(columns[0]))
        course_id.append(int(columns[1]))
        marks.append(int(columns[2]))
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/student_details', methods=['POST'])
def student_details():
    if request.method == 'POST':
        search_type = request.form['search_type']
        if search_type == 'student_id':
            student_id_input = request.form['student_id'].strip()  # Remove leading/trailing whitespace
            if not student_id_input:  # Check if input is empty
                return render_template('student_details_2.html', error_message="Error: Student ID cannot be empty.")
            try:
                student_id_input = int(student_id_input)
            except ValueError:
                return render_template('student_details_2.html', error_message="Error: Invalid input for Student ID.")

            student_data = []
            total_marks = 0
            for i, student in enumerate(student_id):
                if student == student_id_input:
                    student_data.append({'Student id': student, 'Course id': course_id[i], 'Marks': marks[i]})
                    total_marks += marks[i]
            if not student_data:
                return render_template('student_details_2.html', error_message="Error: Student ID not found.")
            return render_template('student_details.html', data=student_data, total_marks=total_marks)
        
        elif search_type == 'course_id':
            course_id_input = request.form['course_id'].strip()
            if not course_id_input:
                return render_template('student_details_2.html', error_message="Error: Student ID cannot be empty.")
            try:
                course_id_input=int(course_id_input)
            except ValueError:
                return render_template('student_details_2.html', error_message="Error: Invalid input for Student ID.")
            ss =[]
            for i, course in enumerate(course_id):
                if course == course_id_input:
                    ss.append(marks[i])
            if not ss:
                return render_template('student_details_2.html', error_message="Error: Invalid input for Student ID.")
            average=sum(ss)/len(ss)
            maxx=max(ss)
            #Generating the histogram
            plt.hist(ss, bins=10, color='skyblue', edgecolor='black')
            plt.xlabel('Marks')
            plt.ylabel('Frequency')
            plt.title('Histogram of Marks')

            # Ensure 'static' folder exists
            static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
            if not os.path.exists(static_folder):
                os.makedirs(static_folder)
            
            # Save histogram image to 'static' folder
            plt.savefig(os.path.join(static_folder, 'image.png'))

            # Clear the current plot to avoid overlapping plots
            plt.clf()

            return render_template('student_details_1.html', data=ss,average=average, maxx=maxx)
    return "Error: Invalid request."
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)