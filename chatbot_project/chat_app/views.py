from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import openai
@csrf_exempt
def ask(request):
    openai.api_key = 'APIキー'

    user_message = request.POST.get('message')
    conversation = request.session.get('conversation', [])     # これまでの会話をセッションから取得
    conversation.append(user_message)     # ユーザーのメッセージを会話に追加
    prompt = " ".join(conversation)     # コンテキストとしてプロンプトを作成
    response = openai.Completion.create(model="text-davinci-003", prompt=prompt, max_tokens=150)
    bot_response = response.choices[0].text.strip()     # Botの応答を会話に追加
    conversation.append(bot_response)
    request.session['conversation'] = conversation     # 更新された会話をセッションに保存
    return JsonResponse({'message': bot_response})
def chat_view(request):
    return render(request, 'chat.html')
