import os
import sys

from backward_chaining import BackwardChaining
from forward_chaining import ForwardChaining
from class_all import *
from class_all import ConvertData


from email.message import EmailMessage
import ssl,smtplib

# biến khởi tạo
person = Person(None, None, None)
validate = Validate()
list_symptom_of_person = []  # list các triệu chứng người dùng khi trả lời là yes

db = ConvertData()
db.convertchanthuong()  # bang chanthuong
db.converttrieuchung()  # bang trieu chung
db.getfc()
db.getbc()
luat_lui = db.groupbc()
luat_tien = db.groupfc()
global position
global time
global yearold
global ever_suffered
global checkttperson
position =''
time = -1
yearold=-1 
ever_suffered= False

#################################################
# 1. câu hỏi chào hỏi
def welcome_question():
    print("-->Chatbot: Xin chào, tôi là chatbot chuẩn đoán chấn thương điền kinh!")
    print("-->Chatbot: Để nhận lời khuyên và chuẩn đoán chi tiết, hãy để lại email, tên và số điện thoại của bạn")

    print("-->Chatbot: hãy nhập tên (gõ 0 để bỏ qua phần cung cấp thông tin)")
    person.name = input() 
    if(person.name == '0'):
        person.name = 'bạn'
        return person
    person.name = validate.validate_name(person.name)
    print(f'-->Người dùng: Tên của tôi là, {person.name}')

    print("-->Chatbot: hãy nhập email(gõ 0 để bỏ qua phần cung cấp thông tin)")
    person.email = input() 
    if(person.email == '0'):
        person.email = None
        return person
    person.email = validate.validate_email(person.email)
    print(f'-->Người dùng: Email của tôi là, {person.email}')

    print("-->Chatbot: hãy nhập số điện thoại(gõ 0 để bỏ qua phần cung cấp thông tin)")  
    person.phoneNumber = input() 
    if(person.phoneNumber == '0'):
        person.phoneNumber = None
        return person
    person.phoneNumber = validate.validate_phonenumber(person.phoneNumber)
    
    print(f'-->Người dùng: số điện thoại của tôi là {person.phoneNumber}')

    print(person)
    return person
# 2. câu hỏi về vị trí nghi ngờ bị chấn thương
def first_question(list_symptom_of_person, person):
    global position
    while (1):
        check = True
        listPosition=['từ đùi tời bẹn', 'bả vai', 'khớp gối', 'lưng', 'cánh tay', 'từ ống đồng tới bàn chân', 'bàn tay']
        if (check):
            print(f'-->Chatbot: {person.name} nếu bạn đang nghi ngờ mình bị trấn thương điền kinh thì hãy giúp tôi trả lời câu hỏi sau.\n Để có chuẩn đoán chính xác, hãy cho tôi biết chi tiết thêm về vị trí bạn cảm thấy đau:')
            print('1. từ đùi tời bẹn ')
            print('2. bả vai')
            print('3. khớp gối')
            print('4. lưng')
            print('5. cánh tay')
            print('6. từ ống đồng tới bàn chân')
            print('7. bàn tay')
            print('0. Vị trí khác')
            print('---------------Câu trả lời của bạn---------------')
            answer = validate.validate_input_number_form(input())
            # print("Người dùng: Lựa chọn của tôi ", answer)
            print(f'-->{person.name}: Lựa chọn của tôi {answer}')
            if (int(answer) < 0 or int(answer) > 7):
                print('-->Chatbot: Vui lòng nhập số từ 0 -> 6')
                continue
            elif (answer == '0'):
                break
            else:
                position=listPosition[int(answer) -1]
                break
        else:
            break

    print(f'-->Chatbot: Chúng tôi đã ghi nhận vị trí {person.name} đang bị chấn thương là:',
          position)
    return list_symptom_of_person

# 3. câu hỏi về thời gian bắt đầu có dấu hiệu chấn thương
def first2_question(list_symptom_of_person, person):
    global time
    while (1):
        check = True
        timeStart =''
        listTime=['', 'trong khoản dưới 1 ngày', 'trong khoảng 1 đến 7 ngày', 'từ 7 ngày trở lên']
        if (check):
            print(f'-->Chatbot: {person.name} có thể cho mình biết thời điểm lần đầu tiên bạn cảm thấy bị đau hoặc có biểu hiện đến bây giờ nằm trong khoảng thời gian nào dưới đây:')
            print('1. trong khoản dưới 1 ngày')
            print('2. trong khoảng 1 đến 7 ngày')
            print('3. từ 7 ngày trở lên')
            print('0. bỏ qua câu hỏi này')
            print('---------------Câu trả lời của bạn---------------')
            answer = validate.validate_input_number_form(input())
            # print("Người dùng: Lựa chọn của tôi ", answer)
            print(f'-->{person.name}: Lựa chọn của tôi {answer}')
            if (int(answer) < 0 or int(answer) > 3):
                print('-->Chatbot: Vui lòng nhập số từ 0 -> 3')
                continue
            elif (answer == '0'):
                break
            else:
                time = answer
                timeStart=listTime[int(answer)]
                break
        else:
            break

    print(f'-->Chatbot: Chúng tôi đã ghi nhận thời gian {person.name} bắt đầu cảm thấy đau hoặc có biểu hiện là:',
          timeStart)
    return list_symptom_of_person
# 4. câu hỏi về tuổi của người sử dụng
def first3_question(list_symptom_of_person, person):
    global yearold
    while (1):
        check = True
        timeStart =''
        listTime=['', 'từ 0 đến 12 tuổi', 'trên 12 đến 18 tuổi', 'trên 18 đến 65 tuổi', 'trên 65 tuổi']
        if (check):
            print(f'-->Chatbot: {person.name} có thể cho mình biết tuổi hiện tại của bạn nằm trong khoảng nào dưới đây:')
            print('1. từ 0 đến 12 tuổi')
            print('2. trên 12 đến 18 tuổi')
            print('3. trên 18 đến 65 tuổi ')
            print('4. trên 65 tuổi ')
            print('0. bỏ qua câu hỏi này')
            print('---------------Câu trả lời của bạn---------------')
            answer = validate.validate_input_number_form(input())
            # print("Người dùng: Lựa chọn của tôi ", answer)
            print(f'-->{person.name}: Lựa chọn của tôi {answer}')
            if (int(answer) < 0 or int(answer) > 4):
                print('-->Chatbot: Vui lòng nhập số từ 0 -> 3')
                continue
            elif (answer == '0'):
                break
            else:
                yearold = answer
                year_old=listTime[int(answer)]
                break
        else:
            break

    print(f'-->Chatbot: Chúng tôi đã ghi nhận độ tuổi của  {person.name} là:',
          year_old)
    return list_symptom_of_person

# 6. câu hỏi liên quan đến cấu dấu hiệu chấn thương xương khớp
def second_question(list_symptom_of_person, person):
    AllSymLst = [db.resulttrieutrung[2], db.resulttrieutrung[3],
                 db.resulttrieutrung[4], db.resulttrieutrung[20], db.resulttrieutrung[11],db.resulttrieutrung[12]
                 ] # chọn các triệu chứng 3,5, 21, 12, 13
    
    NewAllSymLst = []
    for i in AllSymLst:
        NewAllSymLst.append(i["idtrieuchung"])

    while (1):
        if (len(list_symptom_of_person) == len(AllSymLst)):
            break
        print(f'-->Chatbot: Tôi muốn hỏi {person.name} câu hỏi liên quan đến dấu hiệu về xương, khớp để xem bạn có dấu hiệu liên quan đến trấn thương xương, khớp hay không. Bạn có đang gặp một trong các triệu trứng sau hay không(có thể chọn nhiều đáp án):')
        count = 1
        for i in AllSymLst:
            if (i not in list_symptom_of_person):
                print(f'{count}. {i["noidung"]} \n')
            count += 1

        print("0. Tôi không có triệu chứng nào ở trên\n -------------Câu trả lời của bạn--------------")
        answer = validate.validate_input_number_form(input())
        print(f'-->{person.name}: Câu trả lời của tôi là {answer}')

        if (answer == '0'):
            break
        elif (int(answer) < 0 or int(answer) > 6):
            print('-->Chatbot: Vui lòng nhập 1 số từ 0 tới 4')
            continue
        else:
            list_symptom_of_person.append(AllSymLst[int(answer)-1])
        print(
            f'-->Chatbot: Danh sách mã các triệu chứng {person.name} đang mắc:')
        print([i['idtrieuchung'] for i in list_symptom_of_person])
    return list_symptom_of_person

# 7. câu hỏi liên quan đến dấu hiệu chấn thương gân, cơ
def third_question(list_symptom_of_person, person):
    AllSymLst = [db.resulttrieutrung[13], db.resulttrieutrung[15],
                 db.resulttrieutrung[16], db.resulttrieutrung[18]
                 ]
    # chọn các triệu chứng 14, 16, 17, 19 để hỏi
    NewAllSymLst = []
    for i in AllSymLst:
        NewAllSymLst.append(i["idtrieuchung"])

    while (1):
        if (len(list_symptom_of_person) == len(AllSymLst)):
            break
        print(f'-->Chatbot: Tôi muốn hỏi {person.name} câu hỏi liên quan đến tới cơ,dây chằng và gân để xem bạn có dấu hiệu liên quan chấn thương cơ,dây chằng và gân  hay không. Bạn có đang gặp một trong các triệu trứng sau hay không(có thể chọn nhiều đáp án):')
        count = 1
        for i in AllSymLst:
            if (i not in list_symptom_of_person):
                print(f'{count}. {i["noidung"]} \n')
            count += 1

        print("0. Tôi không có triệu chứng nào ở trên\n -------------Câu trả lời của bạn--------------")
        answer = validate.validate_input_number_form(input())
        print(f'-->{person.name}: Câu trả lời của tôi là {answer}')

        if (answer == '0'):
            break
        elif (int(answer) < 0 or int(answer) > 6):
            print('-->Chatbot: Vui lòng nhập 1 số từ 0 tới 4')
            continue
        else:
            list_symptom_of_person.append(AllSymLst[int(answer)-1])
        print(
            f'-->Chatbot: Danh sách mã các triệu chứng {person.name} đang mắc:')
        print([i['idtrieuchung'] for i in list_symptom_of_person])
    return list_symptom_of_person

################################################################
# 8 phần suy diễn tiến
def forward_chaining(rule, fact, goal, file_name,person):
    fc = ForwardChaining(rule, fact, None, file_name)

    list_predicted_disease = [i for i in fc.facts if i[0] == "D"]  # danh sách các bệnh đang nghi  ngờ mắc phải
    print(
        f'-->Chatbot: Chúng tôi dự đoán {person.name} có thể bị chấn thương :', end=" ")
    for i in list_predicted_disease:
        temp = db.get_chanthuong_by_id(i)
        print(temp['tenchanthuong'], end=', ')
    print()
    
    print(
        f'-->Chatbot: Trên đây là chuẩn đoán sơ bộ của chúng tôi. Tiếp theo, chúng tôi sẽ hỏi {person.name} một số câu hỏi để đưa ra kết quả chính xác.', end=" ")
    return list_predicted_disease

########################################################################
# 9 phần suy diễn lùi

def backward_chaining(luat_lui,list_symptom_of_person,list_predicted_disease,file_name ):
    predictD=list_predicted_disease
    rule=luat_lui
    all_rule=db.gettrieuchung()
    fact_real=list_symptom_of_person_id
    chanthuong=0
    for g in predictD:
        goal=g
        D=db.get_chanthuong_by_id(goal) #Chứa thông tin của chấn thương có id == goal
        print(f"Chúng tôi đã có các triệu chứng ban đầu và có thể bạn mắc chấn thương {D['tenchanthuong']}({goal}) , sau đây chúng tôi muốn hỏi bạn một vài câu hỏi để tìm hiểu về chấn thương bạn đang mắc phải")
        all_s_in_D=all_rule[goal]
        all_s_in_D=sorted(set(all_s_in_D)-set(fact_real))
        d=searchindexrule(rule,goal)
        
        b=BackwardChaining(rule,fact_real,goal,file_name) # kết luận trong trường hợp các luât jtruwowsc đã suy ra đk luôn
        
        if b.result1==True:# đoạn đầu
            print("Bạn mắc chấn thương {}- {}và chúng tôi sẽ gửi thêm thông tin về chấn thương này cho bạn qua mail".format(goal,D['tenchanthuong']))
            print(f"Lời khuyên")
            D['loikhuyen']=D['loikhuyen'].replace("/n","\n")
            print(f"{D['loikhuyen']}")
            print("Cám ơn bạn đã sử dụng chat bot của chúng tôi")
            return goal,fact_real
        
        while(len(all_s_in_D)>0):
            s=db.get_trieuchung_by_id(all_s_in_D[0])
            question=f"Bạn có bị triệu chứng {s['noidung']}({all_s_in_D[0]}) không?"
            print(question)
            answer = validate.validate_binary_answer(input())
            
            print(f"answer: {answer}")
            if answer== True :
                fact_real.append(all_s_in_D[0])
                b=BackwardChaining(rule,fact_real,goal,file_name)
                list_no_result,lsD=get_s_in_d(all_s_in_D[0],goal,rule,d,1)
                d=sorted(set(d)-set(lsD))
                all_s_in_D=sorted(set(list_no_result)-set(fact_real))
                if b.result1==True:
                    chanthuong=1
                    break
            if answer==False :
                list_no_result,lsD=get_s_in_d(all_s_in_D[0],goal,rule,d,0) #S01 S02 S03 S04 S05
                d=sorted(set(d)-set(lsD))
                all_s_in_D=sorted(set(list_no_result)-set(fact_real))
            if len(d)==0: 
                print(f"Có vẻ như bạn không mắc chấn thương {goal}-{D['tenchanthuong']}")
                break
        if chanthuong==1:
            print("Bạn mắc chấn thương {}- {} , và chúng tôi sẽ gửi thêm thông tin về chấn thương này cho bạn qua mail".format(goal,D['tenchanthuong']))
            print(f"Lời khuyên")
            D['loikhuyen']=D['loikhuyen'].replace("/n","\n")
            print(f"{D['loikhuyen']}")
            print("Cám ơn bạn đã sử dụng chat bot của chúng tôi")
            
            return goal,fact_real
            break
    if chanthuong==0:
        print(f"Bạn không bị chấn thương nào cả")
        return None, fact_real
def check_the_level(id_chanthuong):
    chanthuong = db.get_chanthuong_by_id(id_chanthuong)
    mess = ''
    if chanthuong['idchanthuong'] == 'D1' or chanthuong['idchanthuong'] or chanthuong['idchanthuong']:
        mess = 'bạn cần phải đến bệnh viện để kiểm tra càng sớm càng tốt'
    elif time == 1:
        mess = 'nếu trong vòng 1 tuần không khỏi và tình trạng ngày càng nặng bạn nên đi gặp bác sĩ'
    elif time == 2:
        mess = 'nếu tình trạng càng trở nên và có thêm nhiều dấu hiệu hơn so với ngày đầu bạn nên đi gặp bác sĩ'
    else:
        mess = 'bạn nên đến gặp bác sĩ để theo dõi, khám và có giải pháp kịp thời'
    return mess

def check_year_old():
    global yearold
    mess = ''
    if yearold == 1:
        mess = 'Trẻ em dưới 12 tuổi có cơ thể đang phát triển, hệ cơ, xương khớp chưa hoàn thiện nên dễ bị chấn thương do sử dụng sai kỹ thuật, tập luyện quá sức, hoặc do va chạm'
    elif time == 2:
        mess = ' Thanh thiếu niên từ 12 đến 18 tuổi đang trong giai đoạn phát triển mạnh, cơ thể bắt đầu cứng cáp hơn nhưng vẫn còn dễ bị chấn thương do tập luyện quá sức hoặc do va chạm '
    elif time == 3:
        mess = 'Người lớn từ 18 đến 65 tuổi có cơ thể đã phát triển hoàn thiện, sức khỏe ổn định hơn nên ít bị chấn thương hơn trẻ em và thanh thiếu niên. Tuy nhiên, người lớn vẫn có thể bị chấn thương do tập luyện quá sức, do va chạm với đối thủ, hoặc do các bệnh lý nền như thoái hóa khớp, viêm khớp'
    else:
        mess = 'Người cao tuổi trên 65 tuổi cơ thể sẽ ngày càng kém đi đặc biệt là về hệ cơ và xương. Người cao tuổi còn dễ bị mắc các bệnh niên quan đến cơ, xương dẫn tới dẫn dê bị chấn thương'
    return mess

#########################################################################
#10 Gửi thông tin qua email
def send_email(list_symptom_of_person_id,id_chanthuong,person):
    global ever_suffered
    email_sender = 'guzamo60@gmail.com'
    email_password = 'paltghsckxotraim'
    email_receiver = person.email
    print(email_receiver)

    chanthuong=db.get_chanthuong_by_id(id_chanthuong)
    benh_trung =''
    # if(ever_suffered == chanthuong['idchanthuong']):
    #     benh_trung='*** Tiền sử: do bạn đã từng mắc bệnh này nên đây có thể là trường hợp tái phát bệnh'
    nguyen_nhan=chanthuong['nguyennhan']
    loi_khuyen=chanthuong['loikhuyen']
    subject='Medical records'
    body=f"""
        ***Xin chào {person.name}
        ***Chúng tôi nhận được các triệu chứng bạn đã gặp phải là : 
        {[db.get_trieuchung_by_id(i)["noidung"] for i in list_symptom_of_person_id]}
        ***Chúng tôi dự đoán bạn bị chấn thương : {chanthuong['tenchanthuong']} vùng {position}
        
        ***Nguyên nhân gây ra chấn thương này là: 
        {nguyen_nhan}
        ***Thông thường ở độ tuổi của bạn  : {check_year_old()}
        ***Qua chuẩn đoán và thời gian bạn cung cấp:
        {check_the_level(id_chanthuong)}
        ***Lời khuyên của chúng tôi dành cho bạn:
        {loi_khuyen}
        ***Cám ơn vì đã dùng Chatbot
    """
    # print(body)
    
    em=EmailMessage()
    em['From']=email_sender
    em['To']=email_receiver
    em['Subject']=subject
    em.set_content(body)
    context=ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp: 
            smtp.login(email_sender,email_password)
            smtp.sendmail(email_sender,email_receiver,em.as_string())
    except:
        print("email không tồn tại")
    

person = welcome_question()
list_symptom_of_person = []  # list các đối tượng triệu chứng

'''
person = Person("None",  "10564165465","huyreeve@gmail.com")
'''
list_symptom_of_person = first_question(list_symptom_of_person, person) # cau hoi ve vi tri
list_symptom_of_person = first2_question(list_symptom_of_person, person) # chay cau hoi ve thoi gian bi chan thuong
list_symptom_of_person = first3_question(list_symptom_of_person, person) # cau hoi ve tuoi cua nguoi su dung
# print([i['idtrieuchung'] for i in list_symptom_of_person])  # list các đối tượng

list_symptom_of_person = second_question(list_symptom_of_person, person)
list_symptom_of_person = third_question(list_symptom_of_person, person)
print([i['idtrieuchung'] for i in list_symptom_of_person])

# list_symptom_of_person = forth_question_before_forward_inference(list_symptom_of_person, person)
# print([i['idtrieuchung'] for i in list_symptom_of_person])

list_symptom_of_person_id = [i['idtrieuchung'] for i in list_symptom_of_person]
list_symptom_of_person_id = list(set(list_symptom_of_person_id))
list_symptom_of_person_id.sort()

list_predicted_disease = forward_chaining(luat_tien, list_symptom_of_person_id, None, 'ex', person)
print(list_predicted_disease)


if len(list_predicted_disease)==0 :
    print("Bạn không có dấu hiệu cảu chấn thương nào cả.Cám ơn bạn đã sử dụng ChatBot")
    sys.exit()

'''list_predicted_disease=['D01','D02','D03']
list_symptom_of_person_id=['S01','S02','S04','S09']'''
disease,list_symptom_of_person_id= backward_chaining(luat_lui,list_symptom_of_person_id,list_predicted_disease,"ex")


'''list_symptom_of_person_id= ['S01','S02']
disease="D01"
person = Person("None",  "10564165465","huyreeve@gmail.com")'''

send_email(list_symptom_of_person_id,disease,person)
