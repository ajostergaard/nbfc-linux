complete -c ec_probe -s h -l help -d 'show this help message and exit'
complete -c ec_probe -s e -l embedded-controller -d 'Specify embedded controller to use' -f -a 'ec_linux ec_sys_linux'
complete -c ec_probe -f -n "not __fish_seen_subcommand_from dump read write monitor" -a dump -d 'Dump all EC registers'
complete -c ec_probe -f -n "not __fish_seen_subcommand_from dump read write monitor" -a read -d 'Read a byte from a EC register'
complete -c ec_probe -f -n "not __fish_seen_subcommand_from dump read write monitor" -a write -d 'Write a byte to a EC register'
complete -c ec_probe -f -n "not __fish_seen_subcommand_from dump read write monitor" -a monitor -d 'Monitor all EC registers for changes'
complete -c ec_probe -n '__fish_seen_subcommand_from dump' -s h -l help -d 'show this help message and exit'
complete -c ec_probe -n '__fish_seen_subcommand_from read' -s h -l help -d 'show this help message and exit'
complete -c ec_probe -n '__fish_seen_subcommand_from read' -d 'Register source' -f -a '0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254'
complete -c ec_probe -n '__fish_seen_subcommand_from write' -s h -l help -d 'show this help message and exit'
complete -c ec_probe -n '__fish_seen_subcommand_from write' -d 'Register destination' -f -a '0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254'
complete -c ec_probe -n '__fish_seen_subcommand_from write' -d 'Value to write' -f -a '0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254'
complete -c ec_probe -n '__fish_seen_subcommand_from monitor' -s h -l help -d 'show this help message and exit'
complete -c ec_probe -n '__fish_seen_subcommand_from monitor' -s i -l interval -d 'Monitored timespan' -f -a "0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 '...'"
complete -c ec_probe -n '__fish_seen_subcommand_from monitor' -s t -l timespan -d 'Set poll intervall' -f -a "0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 '...'"
complete -c ec_probe -n '__fish_seen_subcommand_from monitor' -s r -l report -d 'Save all readings as a CSV file'
complete -c ec_probe -n '__fish_seen_subcommand_from monitor' -s c -l clearly -d 'Blanks out consecutive duplicate readings'
complete -c ec_probe -n '__fish_seen_subcommand_from monitor' -s d -l decimal -d 'Output readings in decimal format instead of hexadecimal format'

