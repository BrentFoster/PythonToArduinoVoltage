img = zeros(256,256);

close all

while true
    for i = 1:1:100

        img = ones(256,256);
        img = img*i;
    %     img(1,1) = 0;

        image(img)
        title(i)
        pause(0.6)   

    end

    for i = 100:-1:1

        img = ones(256,256);
        img = img*i;
    %     img(1,1) = 0;

        image(img)
        title(i)
        pause(0.6)   

    end
end