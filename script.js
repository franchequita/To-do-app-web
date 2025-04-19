let tasks = JSON.parse(localStorage.getItem('tasks')) || [];

const taskForm = document.getElementById('task-form');
const taskInput = document.getElementById('task-input');
const taskList = document.getElementById('task-list');
const taskCounter = document.getElementById('task-counter');
const alertMessage = document.getElementById('alert');

let dragSrcIndex = null;

function saveTasks() {
  localStorage.setItem('tasks', JSON.stringify(tasks));
  updateCounter();
}

function updateCounter() {
  const pending = tasks.filter(t => !t.completed).length;
  taskCounter.textContent = `Tareas pendientes: ${pending}`;
}

function renderTasks() {
  taskList.innerHTML = '';
  tasks.forEach((task, index) => {
    const li = document.createElement('li');
    li.className = `task ${task.completed ? 'completed' : ''}`;
    li.setAttribute('draggable', 'true');
    li.setAttribute('data-index', index);

    // Eventos para drag and drop
    li.addEventListener('dragstart', (e) => {
      dragSrcIndex = index;
      e.dataTransfer.effectAllowed = 'move';
    });

    li.addEventListener('dragover', (e) => {
      e.preventDefault();
    });

    li.addEventListener('drop', (e) => {
      e.preventDefault();
      const targetIndex = +li.getAttribute('data-index');
      if (dragSrcIndex !== null && dragSrcIndex !== targetIndex) {
        const draggedTask = tasks[dragSrcIndex];
        tasks.splice(dragSrcIndex, 1);
        tasks.splice(targetIndex, 0, draggedTask);
        saveTasks();
        renderTasks();
      }
    });

    const span = document.createElement('span');
    span.textContent = task.text;

    const actions = document.createElement('div');
    actions.className = 'actions';

    const completeBtn = document.createElement('button');
    completeBtn.textContent = task.completed ? 'Desmarcar' : 'Completar';
    completeBtn.onclick = () => {
      task.completed = !task.completed;
      saveTasks();
      renderTasks();
    };

    const editBtn = document.createElement('button');
    editBtn.textContent = 'Editar';
    editBtn.onclick = () => {
      const newText = prompt('Editar tarea:', task.text);
      if (newText !== null && newText.trim() !== '') {
        task.text = newText;
        saveTasks();
        renderTasks();
      }
    };

    const deleteBtn = document.createElement('button');
    deleteBtn.textContent = 'Eliminar';
    deleteBtn.classList.add('delete');
    deleteBtn.onclick = () => {
      tasks.splice(index, 1);
      saveTasks();
      renderTasks();
    };

    actions.append(completeBtn, editBtn, deleteBtn);
    li.append(span, actions);
    taskList.appendChild(li);
  });
  updateCounter();
}

taskForm.onsubmit = (e) => {
  e.preventDefault();
  const value = taskInput.value.trim();

  if (value === '') {
    alertMessage.textContent = '⚠️ La tarea no puede estar vacía.';
    return;
  }

  alertMessage.textContent = '';
  tasks.push({ text: value, completed: false });
  taskInput.value = '';
  saveTasks();
  renderTasks();
};

renderTasks();
