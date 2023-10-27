from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from django.http import JsonResponse
import os
import openai



#openai.api_key = os.getenv("OPENAI_API_KEY")

# Create your views here.
class HomePageView(TemplateView):
    template_name = "core/index.html"

class SingInPageView(TemplateView):
    template_name = "core/signin.html"

class SingOutPageView(TemplateView):
    template_name = "core/signout.html"
    
class TestGeneratorView(TemplateView):
    template_name = "core/testGenerator.html"
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        message = request.POST.get('prompt')
        try:
            # Llamar a la función ask_openai para obtener una respuesta de OpenAI
            response = self.ask_openai(message)
            answerFixed = self.fixAnswer(response)
            # Devolver la respuesta en un JSON
            print(4)
            return JsonResponse({'message': message, 'response': answerFixed})
            
        except Exception as e:
            # Manejar cualquier excepción que pueda ocurrir y devolver un mensaje de error
            return JsonResponse({'error': str(e)})
    def fixAnswer(self,answer):
        lineas = answer.strip().split('\n')
        formateado = []

        for linea in lineas:
            linea = linea.strip()
            if linea.startswith("Pregunta"):
                formateado.append("||" + linea[12:])
            elif linea.startswith("{"):
                formateado.append(linea)
            elif linea.startswith("A)") or linea.startswith("B)") or linea.startswith("C)") or linea.startswith("D)") or linea.startswith("ANSWER") or  linea.startswith(""):
                formateado.append("||" + linea)

        return "".join(formateado) + "||"
    def ask_openai(self, message):
        try:
             response = openai.Completion.create(
                 model="text-davinci-003",
                 prompt=message,
                 max_tokens=200,
                 n=1,
                 stop=None,
                 temperature=0.7,
             )
             print("Bien")
             answer = response.choices[0].text.strip()
             print(response)
             return answer
        except Exception as e:
            response = """
                Pregunta 1: ¿Cuál es el nombre del álbum debut de Hozier lanzado en 2014?
                {=Hozier =hozier =Hozier (con inicial mayúscula) =hozier (con inicial mayúscula)}

                Pregunta 2: La canción "Take Me to Church" de Hozier se convirtió en un gran éxito. ¿En qué año fue lanzada?
                {=2013 =Dos mil trece =dos mil trece =2013 (numérico)}

                Pregunta 3: ¿Qué instrumento musical toca Hozier además de cantar?
                {=Guitarra =guitarra =La guitarra =la guitarra}

                Pregunta 4: ¿Cuál es el nombre completo del cantante Hozier?
                {=Andrew John Hozier-Byrne =Andrew Hozier-Byrne =Andrew John Hozier-Byrne (nombre y apellidos completos) =Andrew Hozier-Byrne (nombre y apellidos completos)}

                Pregunta 5: La canción "Someone New" de Hozier incluye la línea "You know it is better than a one-night stand." ¿Cuál es la palabra que falta en la línea?
                {=One =one =1 =uno}

                """
             # Manejar cualquier excepción que pueda ocurrir al interactuar con OpenAI
            print("F")
            return response
        

class TestEditorView(TemplateView):
    template_name = "core/testEditor.html"

class ChatPageView(TemplateView):
    template_name = "core/chat_copy.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        message = request.POST.get('message')

        try:
            # Llamar a la función ask_openai para obtener una respuesta de OpenAI
            response = self.ask_openai(message)

            # Devolver la respuesta en un JSON
            return JsonResponse({'message': message, 'response': response})
        except Exception as e:
            # Manejar cualquier excepción que pueda ocurrir y devolver un mensaje de error
            return JsonResponse({'error': str(e)})

    def ask_openai(self, message):
        print("hola")
        try:
             response = openai.Completion.create(
                 model="text-davinci-003",
                 prompt=message,
                 max_tokens=200,
                 n=1,
                 stop=None,
                 temperature=0.7,
             )
             print(message)
             print("Bien")
             answer = response.choices[0].text.strip()
             print(response)
             return answer
        except Exception as e:
             # Manejar cualquier excepción que pueda ocurrir al interactuar con OpenAI
             return f"Error: {str(e)}"

class TestInstructionsView(TemplateView):
    template_name = "core/TestInstructions.html"
