document.addEventListener('DOMContentLoaded', function() {
  var buttons = document.querySelectorAll('.buttona');
  buttons.forEach(function(button) {
    button.addEventListener('click', function() {
      var buttonText = button.textContent; // Obtiene el texto del botón
      var userInput = document.getElementById('user-input');
      userInput.value = buttonText; // Inserta el texto del botón en el cuadro de "Introduce una pregunta"
    });
  });
  // Obtiene elementos del DOM
  var chatContainer = document.querySelector('.chat-container');
  var userInput = document.getElementById('user-input');
  
  var chatMessages = document.getElementById('chat-messages');
  document.querySelector('.user-input').style.marginTop = '-20%';

  // Oculta los cuadros de botones y el título
  function hideUIElements() {
    var buttonContainer = document.querySelector('.button-container');
    var chatHeader = document.querySelector('.chat-header');
    buttonContainer.style.display = 'none';
    chatHeader.style.display = 'none';
    var logoImage = document.querySelector('.logo-image');
    logoImage.style.display = 'none';
    localStorage.setItem('logoVisible', 'false');
  }

  // Muestra los cuadros de botones y el título
  function showUIElements() {
    document.querySelector('.user-input').style.marginTop = 'auto';
    var buttonsContainer = document.querySelector('.button-container');
    var chatHeader = document.querySelector('.chat-header');
    var userInput = document.querySelector('.user-input');

    buttonsContainer.style.display = 'none';
    chatHeader.style.display = 'none';
    userInput.style.visibility = 'visible';
    userInput.style.position = 'sticky';
    var logoVisible = localStorage.getItem('logoVisible');
    if (logoVisible === 'true') {
      // Muestra la imagen del logo
      var logoImage = document.querySelector('.logo-image');
      logoImage.style.display = 'block';
    } else {
      // Oculta la imagen del logo
      var logoImage = document.querySelector('.logo-image');
      logoImage.style.display = 'none';
    }
    document.querySelector('.image-container').style.display = 'none';
  }

  // Envía la pregunta al servidor
  function sendQuestion(question) {
    fetch('/answer', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ pregunta: question })
    })
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        // Muestra las respuestas en el chat
        var answers = data.split("\n\nFuente:");
        answers.forEach(function (answer) {
          displayAssistantMessage(answer);
        });
        // Muestra los cuadros de botones y el título nuevamente
        showUIElements();
      });
  }

  // Muestra el mensaje del asistente en el chat
  
  // Muestra el mensaje del asistente en el chat
  function displayAssistantMessage(message) {
    var chatMessages = document.getElementById('chat-messages');
    var assistantMessage = document.createElement('div');
    assistantMessage.classList.add('assistant-message');

    // Crea un elemento <div> para el contenedor de la respuesta
    var responseContainer = document.createElement('div');
    responseContainer.classList.add('response-container');

    // Crea un elemento <img> para la imagen
    var image = document.createElement('img');
    image.src = 'https://www.pikpng.com/pngl/m/245-2457723_azure-bot-services-logo-microsoft-bot-framework-logo.png'; // Reemplaza con la ruta de tu imagen
    responseContainer.appendChild(image);

    // Crea un elemento <p> para el mensaje de texto
    var text = document.createElement('p');
    text.textContent = message;
    responseContainer.appendChild(text);

    assistantMessage.appendChild(responseContainer);

    chatMessages.appendChild(assistantMessage);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    var userInput = document.getElementById('user-input');
    userInput.style.visibility = 'visible';
  }


  

  // Maneja el evento de envío del formulario
  function handleSubmit(event) {
    event.preventDefault();
    var question = userInput.value;
    userInput.value = '';
    if (question.trim() !== '') {
      // Oculta los cuadros de botones y el título al enviar la pregunta
      hideUIElements();
  
      // Muestra la pregunta en el chat
      var userMessageElement = document.createElement('div');
      userMessageElement.className = 'user-message';
  
      // Crea un elemento <img> para la imagen de la pregunta
      var questionImage = document.createElement('img');
      questionImage.src = 'https://cdn-icons-png.flaticon.com/512/1077/1077063.png'; // Reemplaza con la ruta de la imagen de la pregunta
      userMessageElement.appendChild(questionImage);
  
      // Crea un elemento <p> para el texto de la pregunta
      var questionText = document.createElement('p');
      questionText.textContent = question;
      userMessageElement.appendChild(questionText);
  
      chatMessages.appendChild(userMessageElement);
  
      // Envia la pregunta al servidor
      sendQuestion(question);
  
      document.querySelector('.user-input').style.marginTop = 'auto';
      document.querySelector('.image-container').style.display = 'none';
    }
    // Limpia el campo de entrada
  }
  
  // Agrega el evento de envío del formulario
  document.querySelector('.user-input .submit-button').addEventListener('click', handleSubmit);

  // Agrega el evento de envío del formulario al presionar Enter
  userInput.addEventListener('keydown', function(event) {
    if (event.keyCode === 13) {
      
      handleSubmit(event);
    }
  });

  // Verifica y muestra el cuadro de "Introduce una pregunta"
  var userInputVisible = localStorage.getItem('userInputVisible');
  if (userInputVisible === 'true') {
    userInput.style.visibility = 'visible';
  }
});
