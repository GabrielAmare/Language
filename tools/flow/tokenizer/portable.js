export default function makeTokenizer(struct) {
  return function tokenizer(text) {
    let state = 0;
    let content = '';
    let at = 0;
    let to = 0;
    let tokens = [];
    const [managers, omits] = struct;
    for (let char of text + '\0') {
      while (char !== null) {
        const manager = managers[state];
        let action = manager[1];
        for (const handler of manager[0]) {
          if (handler[0].includes(char)) {
            action = handler[1];
            break;
          }
        }
        if (!action) {
          throw new SyntaxError();
        }
        if (action[0]) // add
          content += char;
        if (action[1]) // use
          to++
        if (action[2]) // use
          char = null;
        if (action[3]) { // build
          if (!omits.includes(action[3])) {
            let token = {type: action[3], content: content, at: at, to: to};
            tokens.push(token)
          }
          content = '';
          at = to;
        }
        state = action[4];
      }
    }
    return tokens;
  }
}

