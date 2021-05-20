function dtheta = oscillator(t,theta,w0,N,KN)

dtheta = zeros(N,N);
theta = reshape(theta,N,N);

for i = 1:N
    for j = 1:N
    
        theta_diff = theta(i,j) - theta;
        
        % Compute distance matrix D at (i,j)
        a = i*ones(1,N);
        Dx = repmat(abs((1:N) - a),N,1);
        
        b = j*ones(N,1);
        Dy = repmat(abs((1:N)' - b),1,N);
        
        D = sqrt(Dx.^2 + Dy.^2);
        
        % Set Gaussian Wavelet 
%         W = KN/sqrt(2*pi*1)*exp(-1/2 * D.^2 );
        
        % Morlet wavelet
        W = KN*exp(-D.^2/2).*cos(D);
        dtheta(i,j) = w0(i,j) + sum(W.*sin(theta_diff), 'all');
        
    end
end
dtheta = reshape(dtheta,N^2,1);
end
