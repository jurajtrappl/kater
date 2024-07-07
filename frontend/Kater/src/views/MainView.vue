<template>
    <h1>Welcome, {{ data.user.username }}!</h1>
    
    <div>
        <p>Stats</p>
        <h3>Level: {{ data.player.level }}</h3><br />
        <h3>Energy: {{ data.player.energy }}</h3><br />
        <h3>Balance: {{ data.player.balance }}</h3>
    </div>
</template>

<script lang="ts">
import { defineComponent, onBeforeMount, onBeforeUnmount, onMounted, reactive } from 'vue'

interface PlayerData {
    level: number
    energy: number
    balance: number
}

interface UserData {
    username: string
}

interface MainData {
    player: PlayerData
    user: UserData
}

export default defineComponent({
    name: "Main",
    setup() {
        const data: MainData = reactive({
            player: {
                level: 0,
                energy: 0,
                balance: 0
            },
            user: {
                username: ""
            }
        })

        const fetchData = async () => {
            try {
                const response = await fetch("http://localhost:8000/user/", {
                    headers: {
                        "Content-Type": "application/json",
                    },
                    credentials: "include",
                })

                if (response.status === 200) {
                    const content = await response.json()
                    Object.assign(data, content)
                } else {
                    console.log("User problem.")
                }
            } catch (error) {
                console.error("An error occurred: ", error)
            }
        }

        let intervalId: number | undefined
        onMounted(async () => {
            fetchData()
            intervalId = window.setInterval(fetchData, 5000)
        })

        onBeforeUnmount(() => {
            if (intervalId) {
                clearInterval(intervalId)
            }
        })

        return {
            data
        }
    }
})
</script>