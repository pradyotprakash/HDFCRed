awk 'BEGIN{count = 0;count1=0;param=5.0;}{count1++;if($1 >= -param && $1 <= param){count++};}END{print "Within " param "% error: " 100*count/count1}' < err
awk 'BEGIN{count = 0;count1=0;param=10.0;}{count1++;if($1 >= -param && $1 <= param){count++};}END{print "Within " param "% error: " 100*count/count1}' < err
awk 'BEGIN{count = 0;count1=0;param=20.0;}{count1++;if($1 >= -param && $1 <= param){count++};}END{print "Within " param "% error: " 100*count/count1}' < err
awk 'BEGIN{count = 0;count1=0;param=50.0;}{count1++;if($1 >= -param && $1 <= param){count++};}END{print "Within " param "% error: " 100*count/count1}' < err
