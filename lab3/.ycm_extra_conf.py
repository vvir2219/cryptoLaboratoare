def Settings( **kwargs ):
  return {
    'flags': [ '-std=c++17', '-lgmpxx', '-lgmp', '-x', 'c++', '-Wall', '-Wextra', '-Werror' ],
  }
