export type CharacterEmotion = 'neutral' | 'happy' | 'playful' | 'caring' | 'sad' | 'excited';

const EMOTION_KEYWORDS: Record<CharacterEmotion, string[]> = {
  neutral: [],
  happy: ['senang', 'happy', 'bagus', 'keren', 'great', 'mantap', 'nice', 'berhasil', 'good job'],
  playful: ['hehe', 'wkwk', 'iseng', 'teasing', 'nakal', '😜', '😉', 'hihi'],
  caring: ['tenang', 'gapapa', 'aku bantu', 'pelan-pelan', 'you got this', 'jangan khawatir', 'semangat'],
  sad: ['maaf', 'sorry', 'sedih', 'duh', 'sayang sekali', 'kasihan', 'kecewa'],
  excited: ['wow', 'anjir', 'gila', 'seru', 'excited', 'let\'s go', '🔥', '!'],
};

// Expression names available in Alexia.model3.json
const EXPRESSION_MAP: Record<CharacterEmotion, string[]> = {
  neutral: ['bbt', 'k', 'wh'],
  happy: ['h', 'xxy', 'y'],
  playful: ['dyj', 'lzx', 'yjys1'],
  caring: ['yf', 'yfmz', 'mj'],
  sad: ['lh', 'sq', 'zs1'],
  excited: ['yjys2', 'h', 'xxy'],
};

function scoreEmotion(text: string, emotion: CharacterEmotion): number {
  const lower = text.toLowerCase();
  return EMOTION_KEYWORDS[emotion].reduce((score, keyword) => {
    return lower.includes(keyword) ? score + 1 : score;
  }, 0);
}

export function detectAssistantEmotion(text: string): CharacterEmotion {
  if (!text || !text.trim()) {
    return 'neutral';
  }

  const emotions: CharacterEmotion[] = ['happy', 'playful', 'caring', 'sad', 'excited'];
  let best: CharacterEmotion = 'neutral';
  let bestScore = 0;

  for (const emotion of emotions) {
    const score = scoreEmotion(text, emotion);
    if (score > bestScore) {
      best = emotion;
      bestScore = score;
    }
  }

  if (bestScore === 0) {
    if (text.includes('!')) {
      return 'excited';
    }
    if (text.includes('?')) {
      return 'playful';
    }
    return 'neutral';
  }

  return best;
}

function stringHash(input: string): number {
  let hash = 0;
  for (let i = 0; i < input.length; i++) {
    hash = (hash << 5) - hash + input.charCodeAt(i);
    hash |= 0;
  }
  return Math.abs(hash);
}

export function pickExpressionForEmotion(emotion: CharacterEmotion, seedText = ''): string {
  const choices = EXPRESSION_MAP[emotion] || EXPRESSION_MAP.neutral;
  if (choices.length === 1) {
    return choices[0];
  }

  const idx = stringHash(`${emotion}:${seedText}`) % choices.length;
  return choices[idx];
}
