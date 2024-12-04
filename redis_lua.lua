docker exec -it Redis redis-cli EVAL "
local result = {}
local keys = redis.call('KEYS', '*')
for _, key in ipairs(keys) do
    local value = redis.call('GET', key)
    table.insert(result, key)
    table.insert(result, value)
end
return result
" 0
