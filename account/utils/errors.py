def compile_errors(errors):

     print("Here")
     error_list = []
     for key, value in errors.items():
          
          if key in ['address', 'city', 'state', 'country']:
               error_list.append(f'{key.capitalize()} is required')

          elif key == 'email':

               if 'already exists' in value[0]:
                    error_list.append('Email already exists')
               elif 'valid' in value[0]:
                    error_list.append('Invalid Email address')
               else:
                    error_list.append(f'{key.capitalize()} is required')

          elif key == 'password':
               print(key, value[0])
               if 'required' in value[0]:
                    error_list.append('Password is required')
               elif 'common' in value[0]:
                    error_list.append('Password is too common')
               else:
                    error_list.append('Password must be at least 8 characters long')

          elif key == 'username':

               if 'already exists' in value[0]:
                    error_list.append('Username already exists')
               else:
                    error_list.append(f'{key.capitalize()} is required')

          elif key == 'phone':

               if 'already exists' in value[0]:
                    error_list.append('Phone number already exists')
               else:
                    error_list.append(f'{key.capitalize()} is required')

          elif key == 'account_type':

               if 'is not a valid choice' in value[0]:
                    error_list.append('Account type is not valid')
               else:
                    error_list.append(f'{key.capitalize()} is required')

          else:
               error_list.append({key: value[0]})

     return error_list