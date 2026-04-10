<template>
    <div class="toast" :class="type">
        <span class="icon">{{ icon }}</span>
        <span class="message">{{ message }}</span>
    </div>
</template>

<script>
export default {
    name: 'Toast',
    props: {
        type: {
            type: String,
            default: 'info'
        },
        message: {
            type: String,
            required: true
        }
    },
    computed: {
        icon() {
            const icons = {
                success: '[OK]',
                error: '[ERR]',
                info: '[i]'
            }
            return icons[this.type] || '[*]'
        }
    }
}
</script>

<style scoped>
.toast {
    position: fixed;
    bottom: 2rem;
    right: 2rem;
    padding: 1.25rem 1.75rem;
    border-radius: 0.5rem;
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    display: flex;
    align-items: center;
    gap: 1rem;
    animation: slideIn 0.3s ease;
    z-index: 9999;
    font-weight: 600;
}

.toast.success {
    border-left: 3px solid var(--success);
}

.toast.success .icon {
    color: var(--success);
}

.toast.error {
    border-left: 3px solid var(--error);
}

.toast.error .icon {
    color: var(--error);
}

.toast.info .icon {
    color: var(--text-primary);
}

.icon {
    font-weight: 700;
    font-size: 1rem;
    min-width: 40px;
    text-align: center;
}

.message {
    font-size: 0.95rem;
    color: var(--text-primary);
}

@keyframes slideIn {
    from {
        transform: translateX(400px);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}
</style>
