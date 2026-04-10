<template>
    <div class="admin-dashboard">
        <nav class="navbar">
            <div class="nav-content">
                <div class="logo">VC LMS Admin</div>
                <button class="btn btn-secondary btn-sm" @click="$emit('logout')">Logout</button>
            </div>
        </nav>
        
        <div class="container">
            <div class="search-section">
                <h2>Search Students</h2>
                <p class="section-desc">Find and manage student files</p>
                
                <div class="search-inputs">
                    <input 
                        v-model="searchName" 
                        type="text" 
                        placeholder="Search by name"
                        @input="debouncedSearch"
                    >
                    <input 
                        v-model="searchUrn" 
                        type="text" 
                        placeholder="Search by URN"
                        @input="debouncedSearch"
                    >
                </div>
            </div>
            
            <div v-if="loading" class="loading">
                <div class="spinner"></div>
                <p>Loading...</p>
            </div>
            
            <div v-else-if="students.length === 0 && searched" class="empty">
                <p>No students found</p>
            </div>
            
            <div v-else-if="students.length > 0">
                <div class="uploads-section">
                    <h3>Recent Uploads</h3>
                    <div class="uploads-table">
                        <div class="table-header">
                            <div class="col-name">Student Name</div>
                            <div class="col-urn">URN</div>
                            <div class="col-file">File</div>
                            <div class="col-time">Timestamp</div>
                            <div class="col-action">Action</div>
                        </div>
                        <div class="table-body">
                            <div v-for="student in students" :key="student.student_urn" class="table-row">
                                <div class="col-name">{{ student.student_name }}</div>
                                <div class="col-urn">{{ student.student_urn }}</div>
                                <div class="col-file">{{ student.file_count }} file(s)</div>
                                <div class="col-time">-</div>
                                <button class="col-action btn btn-primary btn-sm" @click="selectStudent(student)">
                                    View Files
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <StudentFilesModal 
            v-if="selectedStudent"
            :student="selectedStudent"
            :token="token"
            @close="selectedStudent = null"
            @download="handleDownload"
        />
    </div>
</template>

<script>
import { ref } from 'vue'
import api from '../services/api'
import StudentFilesModal from '../components/StudentFilesModal.vue'

export default {
    name: 'AdminDashboard',
    components: {
        StudentFilesModal
    },
    props: {
        token: String
    },
    emits: ['logout'],
    setup() {
        const searchName = ref('')
        const searchUrn = ref('')
        const students = ref([])
        const loading = ref(false)
        const searched = ref(false)
        const selectedStudent = ref(null)
        let searchTimeout
        
        const performSearch = async () => {
            if (!searchName.value && !searchUrn.value) {
                students.value = []
                searched.value = false
                return
            }
            
            loading.value = true
            try {
                const response = await api.searchStudents(
                    searchName.value || null,
                    searchUrn.value || null
                )
                students.value = response.data.students || []
                searched.value = true
            } catch (error) {
                students.value = []
                searched.value = true
            } finally {
                loading.value = false
            }
        }
        
        const debouncedSearch = () => {
            clearTimeout(searchTimeout)
            searchTimeout = setTimeout(performSearch, 300)
        }
        
        const selectStudent = (student) => {
            selectedStudent.value = student
        }
        
        const handleDownload = async (student_urn, filename) => {
            try {
                const response = await api.adminDownload(student_urn, filename)
                const blob = response.data || response
                const url = URL.createObjectURL(blob)
                const a = document.createElement('a')
                a.href = url
                a.download = filename
                a.click()
                URL.revokeObjectURL(url)
            } catch (error) {
                console.error('Download failed', error)
            }
        }
        
        return {
            searchName,
            searchUrn,
            students,
            loading,
            searched,
            selectedStudent,
            debouncedSearch,
            selectStudent,
            handleDownload
        }
    }
}
</script>

<style scoped>
.admin-dashboard {
    min-height: 100vh;
    background: var(--bg-primary);
}

.navbar {
    background: var(--bg-secondary);
    border-bottom: 1px solid var(--border-color);
    padding: 1.5rem 0;
    position: sticky;
    top: 0;
    z-index: 100;
}

.nav-content {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-primary);
    text-transform: uppercase;
    letter-spacing: 1px;
}

.container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 2rem;
}

.search-section {
    margin-bottom: 3rem;
}

.search-section h2 {
    font-size: 2rem;
    margin-bottom: 0.5rem;
    color: var(--text-primary);
    font-weight: 700;
}

.section-desc {
    color: var(--text-secondary);
    margin-bottom: 1.5rem;
    font-size: 0.95rem;
}

.search-inputs {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
}

@media (max-width: 768px) {
    .search-inputs {
        grid-template-columns: 1fr;
    }
}

.loading, .empty {
    text-align: center;
    padding: 3rem 0;
    color: var(--text-secondary);
}

.uploads-section {
    margin-top: 3rem;
}

.uploads-section h3 {
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
    color: var(--text-primary);
    font-weight: 700;
}

.uploads-table {
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 0.5rem;
    overflow: hidden;
}

.table-header {
    display: grid;
    grid-template-columns: 1.5fr 1fr 1fr 1fr 1fr;
    gap: 1rem;
    padding: 1.5rem;
    background: var(--bg-tertiary);
    border-bottom: 1px solid var(--border-color);
    font-weight: 700;
    color: var(--text-primary);
    font-size: 0.85rem;
}

.table-body {
    display: flex;
    flex-direction: column;
}

.table-row {
    display: grid;
    grid-template-columns: 1.5fr 1fr 1fr 1fr 1fr;
    gap: 1rem;
    padding: 1.5rem;
    border-bottom: 1px solid var(--border-color);
    align-items: center;
    transition: background-color 0.2s ease;
}

.table-row:hover {
    background: var(--bg-tertiary);
}

.table-row:last-child {
    border-bottom: none;
}

.col-name {
    color: var(--text-primary);
    font-weight: 600;
    text-transform: capitalize;
}

.col-urn {
    color: var(--text-secondary);
    font-family: monospace;
    font-size: 0.9rem;
}

.col-file {
    color: var(--text-primary);
    font-weight: 600;
}

.col-time {
    color: var(--text-secondary);
    font-size: 0.9rem;
}

.col-action {
    justify-self: end;
}

@media (max-width: 1024px) {
    .table-header,
    .table-row {
        grid-template-columns: 1fr;
        gap: 0.5rem;
    }
    
    .col-name::before {
        content: 'Name: ';
        color: var(--text-primary);
        font-weight: 700;
    }
}
</style>

