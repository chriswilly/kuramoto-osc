clc;clear all;
N = 32;
w0 = max(min(normrnd(zeros(N,N),ones(N,N)),1),-1);  % consider spread 3 sigma look at fig 1 of +3sigma = +1
theta_0 = zeros(1,N^2);
tspan = [0:0.01:20];
KN = 10;

[t,theta] = ode45(@(t,theta) oscillator(t,theta,w0,N,KN),tspan,theta_0);

% Produce the video
for i = 1:length(tspan)/10
    P = reshape(sin(theta(i*10,:)),N,N)';
    imagesc(P)
    colorbar
    title(['H = sin(theta), K/N = ',num2str(1),', ','t = ',num2str(tspan(i)*10),' seconds']);
    xlabel('X coordinate')
    ylabel('Y coordinate')
    drawnow
    F(i) = getframe(gcf) ;
end

  % create the video writer with 1 fps
  writerObj = VideoWriter('WvLt2_KN_1_5050.avi');
  writerObj.FrameRate = 10;
  % set the seconds per image
% open the video writer
open(writerObj);
% write the frames to the video
for i=1:length(F)
    % convert the image to a frame
    frame = F(i) ;    
    writeVideo(writerObj, frame);
end
% close the writer object
close(writerObj);