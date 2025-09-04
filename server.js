const express = require('express');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// In-memory storage for todos (in production, use a database)
let todos = [
  { id: 1, title: 'Learn Node.js', description: 'Study Node.js fundamentals', completed: false, createdAt: new Date() },
  { id: 2, title: 'Build REST API', description: 'Create a simple REST API with CRUD operations', completed: false, createdAt: new Date() }
];

// Helper function to get next ID
const getNextId = () => {
  return todos.length > 0 ? Math.max(...todos.map(todo => todo.id)) + 1 : 1;
};

// Routes

// GET /todos - Get all todos
app.get('/todos', (req, res) => {
  try {
    res.status(200).json({
      success: true,
      count: todos.length,
      data: todos
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Server Error',
      error: error.message
    });
  }
});

// GET /todos/:id - Get a specific todo by ID
app.get('/todos/:id', (req, res) => {
  try {
    const id = parseInt(req.params.id);
    const todo = todos.find(t => t.id === id);
    
    if (!todo) {
      return res.status(404).json({
        success: false,
        message: 'Todo not found'
      });
    }
    
    res.status(200).json({
      success: true,
      data: todo
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Server Error',
      error: error.message
    });
  }
});

// POST /todos - Create a new todo
app.post('/todos', (req, res) => {
  try {
    const { title, description } = req.body;
    
    // Validation
    if (!title || title.trim() === '') {
      return res.status(400).json({
        success: false,
        message: 'Title is required'
      });
    }
    
    const newTodo = {
      id: getNextId(),
      title: title.trim(),
      description: description ? description.trim() : '',
      completed: false,
      createdAt: new Date(),
      updatedAt: new Date()
    };
    
    todos.push(newTodo);
    
    res.status(201).json({
      success: true,
      message: 'Todo created successfully',
      data: newTodo
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Server Error',
      error: error.message
    });
  }
});

// PUT /todos/:id - Update a todo by ID
app.put('/todos/:id', (req, res) => {
  try {
    const id = parseInt(req.params.id);
    const { title, description, completed } = req.body;
    
    const todoIndex = todos.findIndex(t => t.id === id);
    
    if (todoIndex === -1) {
      return res.status(404).json({
        success: false,
        message: 'Todo not found'
      });
    }
    
    // Update fields if provided
    if (title !== undefined) {
      if (title.trim() === '') {
        return res.status(400).json({
          success: false,
          message: 'Title cannot be empty'
        });
      }
      todos[todoIndex].title = title.trim();
    }
    
    if (description !== undefined) {
      todos[todoIndex].description = description.trim();
    }
    
    if (completed !== undefined) {
      todos[todoIndex].completed = Boolean(completed);
    }
    
    todos[todoIndex].updatedAt = new Date();
    
    res.status(200).json({
      success: true,
      message: 'Todo updated successfully',
      data: todos[todoIndex]
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Server Error',
      error: error.message
    });
  }
});

// DELETE /todos/:id - Delete a todo by ID
app.delete('/todos/:id', (req, res) => {
  try {
    const id = parseInt(req.params.id);
    const todoIndex = todos.findIndex(t => t.id === id);
    
    if (todoIndex === -1) {
      return res.status(404).json({
        success: false,
        message: 'Todo not found'
      });
    }
    
    const deletedTodo = todos.splice(todoIndex, 1)[0];
    
    res.status(200).json({
      success: true,
      message: 'Todo deleted successfully',
      data: deletedTodo
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Server Error',
      error: error.message
    });
  }
});

// Health check endpoint
app.get('/', (req, res) => {
  res.status(200).json({
    success: true,
    message: 'Todo REST API is running!',
    endpoints: {
      'GET /todos': 'Get all todos',
      'GET /todos/:id': 'Get a specific todo',
      'POST /todos': 'Create a new todo',
      'PUT /todos/:id': 'Update a todo',
      'DELETE /todos/:id': 'Delete a todo'
    }
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    success: false,
    message: 'Route not found'
  });
});

// Error handling middleware
app.use((error, req, res, next) => {
  console.error(error.stack);
  res.status(500).json({
    success: false,
    message: 'Something went wrong!',
    error: process.env.NODE_ENV === 'development' ? error.message : 'Internal Server Error'
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
  console.log(`Access the API at: http://localhost:${PORT}`);
  console.log(`Available endpoints:`);
  console.log(`  GET    http://localhost:${PORT}/todos`);
  console.log(`  GET    http://localhost:${PORT}/todos/:id`);
  console.log(`  POST   http://localhost:${PORT}/todos`);
  console.log(`  PUT    http://localhost:${PORT}/todos/:id`);
  console.log(`  DELETE http://localhost:${PORT}/todos/:id`);
});

module.exports = app;