<script setup lang="ts">
import { ref } from 'vue'

defineProps<{
  roomId: string
  roomState: 'waiting' | 'playing' | 'finished' | null
  roomMode: 'ai' | 'pvp' | null
  isCreator: boolean
  playerRole: 'player' | 'spectator' | null
  playerRoleName: string | null
  playerCount: number
  currentTurn: string | null
  currentTurnRole: string | null
  gameResult: string | null
  opponentDisconnected: boolean
  errorMessage: string | null
}>()

const emit = defineEmits<{
  startGame: [initialTurn?: 'A' | 'B', gameMode?: 'normal' | 'endgame']
  terminateMatch: []
  endMatch: []
  leaveRoom: []
}>()

const startPreference = ref<'A' | 'B' | 'random'>('random')
const gameMode = ref<'normal' | 'endgame'>('normal')

function handleStart() {
  const turn = startPreference.value === 'random' ? undefined : startPreference.value
  emit('startGame', turn, gameMode.value)
}

function canStart(
  roomState: string | null,
  isCreator: boolean,
  roomMode: string | null,
  playerCount: number
): boolean {
  if (roomState !== 'waiting' || !isCreator) return false
  if (roomMode === 'pvp') return playerCount >= 2
  return true // ai mode: creator is the only player needed
}

function modeLabel(mode: string | null): string {
  if (mode === 'ai') return '對戰電腦'
  if (mode === 'pvp') return '玩家對戰'
  return ''
}

function roleLabel(role: string | null, roleName: string | null): string {
  if (role === 'player') {
    return '玩家' + (roleName ? ` (${roleName})` : '')
  }
  if (role === 'spectator') return '觀戰者'
  return ''
}

function turnLabel(role: string | null, mode: string | null, turnId: string | null): string {
  if (!role) return ''
  if (mode === 'ai') {
    if (turnId === 'AI_PLAYER') return '電腦'
    return '您'
  }
  return role
}
</script>

<template>
  <div class="w-full max-w-md space-y-3">
    <!-- Room info bar -->
    <div class="flex items-center justify-between rounded-lg bg-white px-4 py-2 shadow-sm">
      <div class="flex items-center gap-3 text-sm text-gray-600">
        <span>房間：<strong class="text-gray-800">{{ roomId }}</strong></span>
        <span class="rounded bg-gray-100 px-2 py-0.5 text-xs">{{ modeLabel(roomMode) }}</span>
        <span class="rounded bg-gray-100 px-2 py-0.5 text-xs">{{ roleLabel(playerRole, playerRoleName) }}</span>
      </div>
      <span class="text-xs text-gray-500">玩家 {{ playerCount }} / {{ roomMode === 'ai' ? 1 : 2 }}</span>
    </div>

    <!-- Turn indicator -->
    <div
      v-if="roomState === 'playing' && currentTurnRole"
      class="rounded-lg bg-blue-50 px-4 py-2 text-center text-sm text-blue-700"
    >
      當前回合：<strong class="font-bold">{{ turnLabel(currentTurnRole, roomMode, currentTurn) }}</strong>
    </div>

    <!-- Waiting message -->
    <div
      v-if="roomState === 'waiting' && roomMode === 'pvp' && playerCount < 2"
      class="rounded-lg bg-yellow-50 px-4 py-2 text-center text-sm text-yellow-700"
    >
      等待其他玩家加入...（{{ playerCount }} / 2）
    </div>

    <!-- Opponent disconnected warning -->
    <div
      v-if="opponentDisconnected"
      class="rounded-lg bg-red-50 px-4 py-2 text-center text-sm text-red-700"
    >
      對手已斷線，10 秒內未重連將判定您獲勝
    </div>

    <!-- Game result -->
    <div
      v-if="roomState === 'finished' && gameResult"
      class="rounded-lg bg-green-50 px-4 py-2 text-center text-sm font-semibold text-green-800"
    >
      {{ gameResult }}
    </div>

    <!-- Error message -->
    <div
      v-if="errorMessage"
      class="rounded-lg bg-red-50 px-4 py-2 text-center text-sm text-red-600"
    >
      {{ errorMessage }}
    </div>

    <!-- Start preference (AI mode only, before start) -->
    <div
      v-if="canStart(roomState, isCreator, roomMode, playerCount) && roomMode === 'ai'"
      class="rounded-lg bg-white px-4 py-2 shadow-sm"
    >
      <div class="mb-2 text-xs font-semibold text-gray-500">選擇先手</div>
      <div class="flex items-center gap-4">
        <label class="flex items-center gap-1.5 text-sm text-gray-600 cursor-pointer">
          <input v-model="startPreference" type="radio" value="random" class="accent-amber-600" />
          隨機
        </label>
        <label class="flex items-center gap-1.5 text-sm text-gray-600 cursor-pointer">
          <input v-model="startPreference" type="radio" value="A" class="accent-amber-600" />
          玩家先行
        </label>
        <label class="flex items-center gap-1.5 text-sm text-gray-600 cursor-pointer">
          <input v-model="startPreference" type="radio" value="B" class="accent-amber-600" />
          電腦先行
        </label>
      </div>
    </div>

    <!-- Game Mode (before start) -->
    <div
      v-if="canStart(roomState, isCreator, roomMode, playerCount)"
      class="rounded-lg bg-white px-4 py-2 shadow-sm"
    >
      <div class="mb-2 text-xs font-semibold text-gray-500">棋局模式</div>
      <div class="flex items-center gap-4">
        <label class="flex items-center gap-1.5 text-sm text-gray-600 cursor-pointer">
          <input v-model="gameMode" type="radio" value="normal" class="accent-amber-600" />
          一般模式
        </label>
        <label class="flex items-center gap-1.5 text-sm text-gray-600 cursor-pointer">
          <input v-model="gameMode" type="radio" value="endgame" class="accent-amber-600" />
          殘局模式
        </label>
      </div>
      <div v-if="gameMode === 'endgame'" class="mt-1 text-sm font-medium text-amber-600">
        * 殘局模式固定由黑棋先手
      </div>
    </div>

    <!-- Action buttons -->
    <div class="flex flex-wrap gap-2">
      <!-- Start game -->
      <button
        v-if="canStart(roomState, isCreator, roomMode, playerCount)"
        @click="handleStart"
        class="rounded bg-green-600 px-4 py-1.5 text-sm font-medium text-white hover:bg-green-700"
      >
        開始比賽
      </button>

      <!-- Terminate match (During play, for creator) -->
      <button
        v-if="roomState === 'playing' && isCreator"
        @click="emit('terminateMatch')"
        class="rounded bg-red-600 px-4 py-1.5 text-sm font-medium text-white hover:bg-red-700"
      >
        中斷比賽
      </button>

      <!-- Leave room / End match (Always available) -->
      <button
        @click="isCreator ? emit('endMatch') : emit('leaveRoom')"
        class="rounded border border-gray-300 px-4 py-1.5 text-sm font-medium text-gray-700 hover:bg-gray-100"
      >
        結束對戰
      </button>
    </div>
  </div>
</template>
