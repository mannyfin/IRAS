function []=layer()

screen=get(0,'screensize');
screen=screen(3:4);
handle.figure=figure(...
    'Name', 'Layer',...
    'NumberTitle', 'off',...
    'color',[.94,.94,.94],...
    'position',[0*screen(1),0.02*screen(2),screen(1),0.9*screen(2)]);
%Axes
%Axes
handle.axes=axes(...
    'units','normalized',...
    'position',[0.36,0.5,0.38,0.45]);
handle.axes2=axes(...
    'units','normalized',...
    'position',[0.36,0.10,0.38,0.3]);
handle.parameters=uipanel(...
    'Title', 'Parameters',...
    'backgroundcolor',[.94,.94,.94],...
    'position', [0.76,0.23,0.23,0.65]);
%Table
columnname={'n','Ia/Iabulk','Is/Isbulk','(Ia*Isbulk)/(Is*Iabulk)'};
columnformat={'numeric','numeric','numeric','numeric'};
handle.table=uitable(...
    'units','normalized',...
    'position', [0.039 0.11 0.25 0.25],...
    'ColumnName', columnname,...
    'ColumnFormat', columnformat,...
    'RowName', []);

%strings with equations
textbox
    function []=textbox()
        handle.newtextbox=axes(...
            'units','normalized',...
            'position',[0.0125,0.41,0.31,0.57],...
            'xtick',[], 'ytick', [],...
            'xcolor', 'w', 'ycolor','w');
        str(1)= {'========= AES Plots ========='};
        str(2)={'Frank-van der Merwe (FM) or layer by layer'};
        str(3)={'growth mode of an ultrathin metal film onto'};
        str(4)={'a dissimilar metal substrate can be monitored'};
        str(5)={'by AES signal intensity, given by: '};
        str(6)={''};
        str(7)={'$$ \frac{I_A(n)}{I_A^{bulk}}=1-exp(-\frac{n*d} {\lambda_A*cos(\theta)}) $$'};
        str(8)={''};
        str(9)={'$$ \frac{I_s(n)}{I_s^{bulk}}=exp(-\frac{n*d} {\lambda_S*cos(\theta)}) $$'};
        str(10)={''};
        str(11)={'$$ I_A(n)$$ = adsorbate signal'};
        str(12)={'$$ I_S(n)$$ = substrate signal'};
        str(13)={'$$I_A^{bulk}$$ = bulk adsorbate signal'};
        str(14)={'$$I_S^{bulk}$$ = bulk substrate signal'};
        str(15)={' n=number of layers '};
        str(16)={'d=monolayer thickness '};
        str(17)={'$$ \lambda_A $$ = IMFP of adsorbate electrons'};
        str(18)={'$$ \lambda_S $$ = IMFP of substrate electrons'};
        str(19)={'$$ \theta $$ = analyzer collection angle'};
        
        
        set(handle.figure,'currentaxes',handle.newtextbox);
        ltxstr=text('Interpreter','latex','string',str, 'units','normalized','position',[.05 .5],'fontsize',16);
    end

%--------------------------------------------------------------------------
%Edit boxes for parameters

%Reaction Order
handle.lambdaa=uicontrol(...
    'style','edit',...
    'units', 'normalized',...
    'string', '7.2',...
    'position', [.1 .83 .3 .1],...
    'parent', handle.parameters,...
    'backgroundcolor', 'w');
uicontrol(...
    'style', 'text',...
    'parent', handle.parameters,...
    'units', 'normalized',...
    'string', 'Lambda A (A)',...
    'position', [0.1,0.73,0.3,0.1]);

%Pre Exponential
handle.lambdas=uicontrol(...
    'style','edit',...
    'units', 'normalized',...
    'string', '5.4',...
    'position', [.6 .83 .3 .1],...
    'parent', handle.parameters,...
    'backgroundcolor', 'w');
uicontrol(...
    'style', 'text',...
    'parent', handle.parameters,...
    'units', 'normalized',...
    'string', 'Lambda S (A)',...
    'position', [0.6,0.73,0.3,0.1]);

% Initial Temperature
handle.numlayers=uicontrol(...
    'style','edit',...
    'units', 'normalized',...
    'string', '6',...
    'position', [.1 .6 .3 .1],...
    'parent', handle.parameters,...
    'backgroundcolor', 'w');
uicontrol(...
    'style', 'text',...
    'parent', handle.parameters,...8
    'units', 'normalized',...
    'string', 'Number of Layers, n',...
    'position', [0.1,0.5,0.3,0.1]);

% Final Temperature
handle.thickness=uicontrol(...
    'style','edit',...
    'units', 'normalized',...
    'string', '2.25',...
    'position', [.6 .6 .3 .1],...
    'parent', handle.parameters,...
    'backgroundcolor', 'w');
uicontrol(...
    'style', 'text',...
    'parent', handle.parameters,...
    'units', 'normalized',...
    'string', 'Monolayer Thickness, d (A)',...
    'position', [0.6,0.5,0.3,0.1]);



% Analyzer collection angle
handle.theta=uicontrol(...
    'style','edit',...
    'units', 'normalized',...
    'string', '20',...
    'position', [.35 .35 .3 .1],...
    'parent', handle.parameters,...
    'backgroundcolor', 'w');
uicontrol(...
    'style', 'text',...
    'parent', handle.parameters,...
    'units', 'normalized',...
    'string', 'Analyzer collector angle, theta (degrees)',...
    'position', [0.35,0.25,0.3,0.1]);
%create plot button
handle.plotit=uicontrol(...
    'style','pushbutton',...
    'units','normalized',...
    'position',[.83 .26 .1 .08],...
    'string','Plot');

%assign callbacks
set(handle.plotit,'callback',{@layerz})

    function []=layerz(varargin)
        hold off
        [lambdaa,lambdas,nuser,theta,dd]=getstuff();
        n=0:nuser;
        lambdaA=lambdaa*1E-10;
        lambdaS=lambdas*1E-10;
        d=dd*1E-10;
        costheta=cosd(theta);
        n1=nuser;
              
                
        for i=1:length(n)
            IaIab(i)=1-exp(-n(i)*d/(lambdaA*costheta));
            IsIsb(i)=exp(-n(i)*d/lambdaS*costheta);
            IaIs(i)=IaIab(i)./IsIsb(i);
        end

        for m=1:n1
            xxx=linspace(0,n1+1,(n1+1)*100);
            a=(m-1)*100+1;
            b=m*100;
            xxxx(m,:)=xxx(a:b);
        end
        [e,f]=size(xxxx);
        
        for i=1:e
            y(i,:)=(IaIab(i)-IaIab(i+1))/(n(i)-n(i+1)).*(xxxx(i,:)-n(i))+IaIab(i);
            z(i,:)=(IsIsb(i)-IsIsb(i+1))/(n(i)-n(i+1)).*(xxxx(i,:)-n(i))+IsIsb(i);
        end
        
        xx=y./z;
        
        
        set(handle.figure,'currentaxes',handle.axes')

        
        for i=1:n1
            xxxx1((((i-1)*100)+1):i*100)=xxxx(i,:);
            y1((((i-1)*100)+1):i*100)=y(i,:);
            z1((((i-1)*100)+1):i*100)=z(i,:);
            x1((((i-1)*100)+1):i*100)=xx(i,:);
        end
        
        dataz=horzcat(xxxx1',y1',z1',x1');
        plot(dataz(:,1),dataz(:,2:3))
        xlabel('Number of layers (n)')
        ylabel('AES signal')
        title('AES Signal Plot for Adsorbate and Substrate Signals')
        legend('show')
        legend('Ia/Iabulk','Is/Isbulk')
        legend('location','best')
        
        set(handle.table,'data',dataz)
        
        set(handle.figure,'currentaxes',handle.axes2)
        plot(dataz(:,1),dataz(:,4))
        xlabel('Number of layers (n)')
        ylabel('AES signal')
        title('Ia*Isbulk/(Is*Iabulk)')
        legend('show')
        legend('Ia*Isbulk/(Is*Iabulk)')
        legend('location','best')
        textbox        
    end


    function [lambdaa,lambdas,nuser,theta,dd]=getstuff(varargin)
        lambdaa=str2double(get(handle.lambdaa,'string'));
        lambdas=str2double(get(handle.lambdas,'string'));
        nuser=str2double(get(handle.numlayers,'string'));
        dd=str2double(get(handle.thickness,'string'));
        theta=str2double(get(handle.theta,'string'));
    end
end
