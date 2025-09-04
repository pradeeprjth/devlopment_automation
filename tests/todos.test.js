const request = require('supertest');
const app = require('../server');

describe('Todo REST API', () => {
  describe('GET /', () => {
    it('should return API information and available endpoints', async () => {
      const res = await request(app)
        .get('/')
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(res.body.message).toBe('Todo REST API is running!');
      expect(res.body.endpoints).toBeDefined();
      expect(res.body.endpoints['GET /todos']).toBe('Get all todos');
    });
  });

  describe('GET /todos', () => {
    it('should return all todos with success response', async () => {
      const res = await request(app)
        .get('/todos')
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(res.body.count).toBeDefined();
      expect(Array.isArray(res.body.data)).toBe(true);
      expect(res.body.data.length).toBeGreaterThanOrEqual(0);
    });

    it('should return todos with correct structure', async () => {
      const res = await request(app)
        .get('/todos')
        .expect(200);

      if (res.body.data.length > 0) {
        const todo = res.body.data[0];
        expect(todo).toHaveProperty('id');
        expect(todo).toHaveProperty('title');
        expect(todo).toHaveProperty('description');
        expect(todo).toHaveProperty('completed');
        expect(todo).toHaveProperty('createdAt');
      }
    });
  });

  describe('GET /todos/:id', () => {
    it('should return a specific todo by ID', async () => {
      // First, get all todos to find a valid ID
      const todosRes = await request(app).get('/todos');
      
      if (todosRes.body.data.length > 0) {
        const todoId = todosRes.body.data[0].id;
        
        const res = await request(app)
          .get(`/todos/${todoId}`)
          .expect(200);

        expect(res.body.success).toBe(true);
        expect(res.body.data).toBeDefined();
        expect(res.body.data.id).toBe(todoId);
      }
    });

    it('should return 404 for non-existent todo', async () => {
      const res = await request(app)
        .get('/todos/99999')
        .expect(404);

      expect(res.body.success).toBe(false);
      expect(res.body.message).toBe('Todo not found');
    });

    it('should handle invalid ID format gracefully', async () => {
      const res = await request(app)
        .get('/todos/invalid-id')
        .expect(404);

      expect(res.body.success).toBe(false);
    });
  });

  describe('POST /todos', () => {
    it('should create a new todo with valid data', async () => {
      const newTodo = {
        title: 'Test Todo',
        description: 'This is a test todo'
      };

      const res = await request(app)
        .post('/todos')
        .send(newTodo)
        .expect(201);

      expect(res.body.success).toBe(true);
      expect(res.body.message).toBe('Todo created successfully');
      expect(res.body.data).toBeDefined();
      expect(res.body.data.title).toBe(newTodo.title);
      expect(res.body.data.description).toBe(newTodo.description);
      expect(res.body.data.completed).toBe(false);
      expect(res.body.data.id).toBeDefined();
      expect(res.body.data.createdAt).toBeDefined();
      expect(res.body.data.updatedAt).toBeDefined();
    });

    it('should create a todo with title only', async () => {
      const newTodo = {
        title: 'Simple Todo'
      };

      const res = await request(app)
        .post('/todos')
        .send(newTodo)
        .expect(201);

      expect(res.body.success).toBe(true);
      expect(res.body.data.title).toBe(newTodo.title);
      expect(res.body.data.description).toBe('');
    });

    it('should return 400 for missing title', async () => {
      const newTodo = {
        description: 'Todo without title'
      };

      const res = await request(app)
        .post('/todos')
        .send(newTodo)
        .expect(400);

      expect(res.body.success).toBe(false);
      expect(res.body.message).toBe('Title is required');
    });

    it('should return 400 for empty title', async () => {
      const newTodo = {
        title: '   ',
        description: 'Todo with empty title'
      };

      const res = await request(app)
        .post('/todos')
        .send(newTodo)
        .expect(400);

      expect(res.body.success).toBe(false);
      expect(res.body.message).toBe('Title is required');
    });

    it('should trim whitespace from title and description', async () => {
      const newTodo = {
        title: '  Trimmed Todo  ',
        description: '  This should be trimmed  '
      };

      const res = await request(app)
        .post('/todos')
        .send(newTodo)
        .expect(201);

      expect(res.body.data.title).toBe('Trimmed Todo');
      expect(res.body.data.description).toBe('This should be trimmed');
    });
  });

  describe('PUT /todos/:id', () => {
    let todoId;

    beforeEach(async () => {
      // Create a todo for testing updates
      const newTodo = {
        title: 'Todo to Update',
        description: 'Original description'
      };

      const res = await request(app)
        .post('/todos')
        .send(newTodo);

      todoId = res.body.data.id;
    });

    it('should update todo title', async () => {
      const updateData = {
        title: 'Updated Todo Title'
      };

      const res = await request(app)
        .put(`/todos/${todoId}`)
        .send(updateData)
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(res.body.message).toBe('Todo updated successfully');
      expect(res.body.data.title).toBe(updateData.title);
      expect(res.body.data.updatedAt).toBeDefined();
    });

    it('should update todo description', async () => {
      const updateData = {
        description: 'Updated description'
      };

      const res = await request(app)
        .put(`/todos/${todoId}`)
        .send(updateData)
        .expect(200);

      expect(res.body.data.description).toBe(updateData.description);
    });

    it('should update todo completion status', async () => {
      const updateData = {
        completed: true
      };

      const res = await request(app)
        .put(`/todos/${todoId}`)
        .send(updateData)
        .expect(200);

      expect(res.body.data.completed).toBe(true);
    });

    it('should update multiple fields at once', async () => {
      const updateData = {
        title: 'Completely Updated Todo',
        description: 'New description',
        completed: true
      };

      const res = await request(app)
        .put(`/todos/${todoId}`)
        .send(updateData)
        .expect(200);

      expect(res.body.data.title).toBe(updateData.title);
      expect(res.body.data.description).toBe(updateData.description);
      expect(res.body.data.completed).toBe(updateData.completed);
    });

    it('should return 404 for non-existent todo', async () => {
      const updateData = {
        title: 'Updated Title'
      };

      const res = await request(app)
        .put('/todos/99999')
        .send(updateData)
        .expect(404);

      expect(res.body.success).toBe(false);
      expect(res.body.message).toBe('Todo not found');
    });

    it('should return 400 for empty title', async () => {
      const updateData = {
        title: '   '
      };

      const res = await request(app)
        .put(`/todos/${todoId}`)
        .send(updateData)
        .expect(400);

      expect(res.body.success).toBe(false);
      expect(res.body.message).toBe('Title cannot be empty');
    });

    it('should handle boolean conversion for completed field', async () => {
      const updateData = {
        completed: 'true'
      };

      const res = await request(app)
        .put(`/todos/${todoId}`)
        .send(updateData)
        .expect(200);

      expect(res.body.data.completed).toBe(true);
    });
  });

  describe('DELETE /todos/:id', () => {
    let todoId;

    beforeEach(async () => {
      // Create a todo for testing deletion
      const newTodo = {
        title: 'Todo to Delete',
        description: 'This todo will be deleted'
      };

      const res = await request(app)
        .post('/todos')
        .send(newTodo);

      todoId = res.body.data.id;
    });

    it('should delete an existing todo', async () => {
      const res = await request(app)
        .delete(`/todos/${todoId}`)
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(res.body.message).toBe('Todo deleted successfully');
      expect(res.body.data).toBeDefined();
      expect(res.body.data.id).toBe(todoId);

      // Verify the todo is actually deleted
      await request(app)
        .get(`/todos/${todoId}`)
        .expect(404);
    });

    it('should return 404 for non-existent todo', async () => {
      const res = await request(app)
        .delete('/todos/99999')
        .expect(404);

      expect(res.body.success).toBe(false);
      expect(res.body.message).toBe('Todo not found');
    });

    it('should handle invalid ID format gracefully', async () => {
      const res = await request(app)
        .delete('/todos/invalid-id')
        .expect(404);

      expect(res.body.success).toBe(false);
    });
  });

  describe('Error Handling', () => {
    it('should return 404 for non-existent routes', async () => {
      const res = await request(app)
        .get('/non-existent-route')
        .expect(404);

      expect(res.body.success).toBe(false);
      expect(res.body.message).toBe('Route not found');
    });

    it('should handle malformed JSON in POST requests', async () => {
      const res = await request(app)
        .post('/todos')
        .send('invalid json')
        .set('Content-Type', 'application/json')
        .expect(500); // Express returns 500 for malformed JSON
    });

    it('should handle malformed JSON in PUT requests', async () => {
      const res = await request(app)
        .put('/todos/1')
        .send('invalid json')
        .set('Content-Type', 'application/json')
        .expect(500); // Express returns 500 for malformed JSON
    });
  });

  describe('Integration Tests', () => {
    it('should handle a complete todo lifecycle', async () => {
      // Create a todo
      const newTodo = {
        title: 'Lifecycle Test Todo',
        description: 'Testing complete lifecycle'
      };

      const createRes = await request(app)
        .post('/todos')
        .send(newTodo)
        .expect(201);

      const todoId = createRes.body.data.id;

      // Read the todo
      const getRes = await request(app)
        .get(`/todos/${todoId}`)
        .expect(200);

      expect(getRes.body.data.title).toBe(newTodo.title);

      // Update the todo
      const updateData = {
        title: 'Updated Lifecycle Todo',
        completed: true
      };

      const updateRes = await request(app)
        .put(`/todos/${todoId}`)
        .send(updateData)
        .expect(200);

      expect(updateRes.body.data.title).toBe(updateData.title);
      expect(updateRes.body.data.completed).toBe(true);

      // Delete the todo
      await request(app)
        .delete(`/todos/${todoId}`)
        .expect(200);

      // Verify deletion
      await request(app)
        .get(`/todos/${todoId}`)
        .expect(404);
    });

    it('should maintain data consistency across operations', async () => {
      // Get initial count
      const initialRes = await request(app).get('/todos');
      const initialCount = initialRes.body.count;

      // Create multiple todos
      const todo1 = await request(app)
        .post('/todos')
        .send({ title: 'Todo 1' });

      const todo2 = await request(app)
        .post('/todos')
        .send({ title: 'Todo 2' });

      // Verify count increased
      const afterCreateRes = await request(app).get('/todos');
      expect(afterCreateRes.body.count).toBe(initialCount + 2);

      // Delete one todo
      await request(app)
        .delete(`/todos/${todo1.body.data.id}`)
        .expect(200);

      // Verify count decreased
      const afterDeleteRes = await request(app).get('/todos');
      expect(afterDeleteRes.body.count).toBe(initialCount + 1);

      // Clean up
      await request(app)
        .delete(`/todos/${todo2.body.data.id}`);
    });
  });
});