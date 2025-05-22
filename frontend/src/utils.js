const verifyUsername = (username) => {
  const errors = []
  const minLength = 3
  const maxLength = 20
  const specialChars = /[!@#$%^&*(),.?":{}|<>]/g

  if (username.length < minLength || username.length > maxLength) {
    errors.push(`Username must be between ${minLength} and ${maxLength} characters long.`)
  }
  if (specialChars.test(username)) {
    errors.push('Username must not contain special characters.')
  }
  if (username.trim() === '') {
    errors.push('Username must not be empty.')
  }
  if (username.includes(' ')) {
    errors.push('Username must not contain spaces.')
  }

  return errors
}

const verifyPassword = (password) => {
  const errors = []
  const minLength = 8
  const maxLength = 20
  const specialChars = /[!@#$%^&*(),.?":{}|<>]/g

  if (password.length < minLength || password.length > maxLength) {
    errors.push(`Password must be between ${minLength} and ${maxLength} characters long.`)
  }
  if (!specialChars.test(password)) {
    errors.push('Password must contain at least one special character.')
  }
  if (password.trim() === '') {
    errors.push('Password must not be empty.')
  }

  return errors
}

export { verifyUsername, verifyPassword }