<template>
    <div class="login-container">
        <div class="backdrop"></div>
        
        <div class="login-card">
            <button class="back-btn" @click="$emit('back')">Back</button>
            
            <div class="header">
                <h2>VC LMS</h2>
                <p class="subtitle">Student Portal Access</p>
            </div>
            
            <form @submit.prevent="handleLogin">
                <div class="form-group">
                    <label>Student Name</label>
                    <input 
                        v-model="studentName" 
                        type="text" 
                        placeholder="Enter your full name"
                        required
                    >
                </div>
                
                <div class="form-group">
                    <label>Student URN</label>
                    <input 
                        v-model="studentUrn" 
                        type="text" 
                        placeholder="Enter your URN (e.g., S12345)"
                        required
                    >
                </div>
                
                <button 
                    type="submit" 
                    class="btn btn-primary btn-login"
                    :disabled="loading"
                >
                    {{ loading ? 'Authenticating...' : 'Access Files' }}
                </button>
            </form>
        </div>
    </div>
</template>

<script>
import { ref } from 'vue'

export default {
    name: 'StudentLogin',
    emits: ['login', 'back'],
    setup(props, { emit }) {
        const studentName = ref('')
        const studentUrn = ref('')
        const loading = ref(false)
        
        const handleLogin = async () => {
            loading.value = true
            try {
                emit('login', studentName.value, studentUrn.value)
            } finally {
                loading.value = false
            }
        }
        
        return {
            studentName,
            studentUrn,
            loading,
            handleLogin
        }
    }
}
</script>

<style scoped>
.login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 2rem;
    position: relative;
    background: var(--bg-primary);
}

.backdrop {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    pointer-events: none;
}

.login-card {
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 0.5rem;
    padding: 4rem 3.5rem;
    width: 100%;
    max-width: 650px;
    position: relative;
    z-index: 1;
    transition: border-color 0.3s ease;
}

.login-card:hover {
    border-color: var(--accent-color);
}

.back-btn {
    position: absolute;
    top: 1.5rem;
    left: 1.5rem;
    background: transparent;
    border: 1px solid var(--border-color);
    color: var(--text-primary);
    cursor: pointer;
    font-size: 0.9rem;
    padding: 0.5rem 1rem;
    border-radius: 0.4rem;
    transition: border-color 0.2s ease;
    font-weight: 600;
}

.back-btn:hover {
    border-color: var(--accent-color);
}

.header {
    text-align: center;
    margin-bottom: 2.5rem;
}

h2 {
    font-size: 2rem;
    color: var(--text-primary);
    margin: 0;
    font-weight: 700;
}

.subtitle {
    color: var(--text-secondary);
    margin: 0.5rem 0 0 0;
    font-size: 0.95rem;
}

.form-group {
    margin-bottom: 1.75rem;
}

label {
    display: block;
    margin-bottom: 0.75rem;
    font-weight: 600;
    font-size: 0.95rem;
    color: var(--text-primary);
}

input {
    width: 100%;
    padding: 0.75rem 1rem;
    background: var(--bg-tertiary);
    border: 1px solid var(--border-color);
    color: var(--text-primary);
    border-radius: 0.4rem;
    font-size: 1rem;
    transition: border-color 0.2s ease;
}

input:focus {
    outline: none;
    border-color: var(--accent-color);
    background: var(--bg-tertiary);
}

input::placeholder {
    color: var(--text-secondary);
}

.btn-login {
    width: 100%;
    margin-top: 1.5rem;
    padding: 1rem;
    font-size: 1rem;
}
</style>
