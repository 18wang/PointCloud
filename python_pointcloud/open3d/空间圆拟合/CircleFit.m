%p0=[-246.786, 127.156, -4937.534];
%p1=[-298.728, 134.548, -4868.401];
%p2=[-372.539, 142.416, -4789.605];
%����̶�����ת��ϳ��켣Բ
%����PΪ�˶��켣�� ��ʽ��ά����
%���a,bΪԲ�ĵ�ƽ������ rΪ�뾶
%angle�ǵ�һ���㵽���һ������˶��Ƕ�
function c=CircleFit(P)
len=size(P);
fy_x=P(:,1);fy_y=P(:,2);fy_z=P(:,3);f=-ones(len(1),1);
PlaneMatrix=[dot(fy_x,fy_x),dot(fy_x,fy_y),dot(fy_x,fy_z);
    dot(fy_y,fy_x),dot(fy_y,fy_y),dot(fy_y,fy_z);
    dot(fy_z,fy_x),dot(fy_z,fy_y),dot(fy_z,fy_z)];
Planef=[dot(fy_x,f);dot(fy_y,f);dot(fy_z,f)];
PlaneFar=PlaneMatrix\Planef;
%ͶӰ��ƽ����
P=Project2Plane(PlaneFar,P);
O=[0,0,0];
O=Project2Plane(PlaneFar,O);
%�ռ�任
n=PlaneFar/norm(PlaneFar);
n=n';
m=(O-P(1,:))/norm(O-P(1,:));
l=cross(m,n);
l=l/norm(l);
EW=[m;l;n];
WE=EW';
PE=P*WE;%�任
fy_a=PE(:,1);
fy_b=PE(:,2);
fy_c=f;
fy_f=fy_a.*fy_a+fy_b.*fy_b;
CircleMatrix=[dot(fy_a,fy_a),dot(fy_a,fy_b),dot(fy_a,fy_c);
    dot(fy_b,fy_a),dot(fy_b,fy_b),dot(fy_b,fy_c);
    dot(fy_c,fy_a),dot(fy_c,fy_b),dot(fy_c,fy_c)];
Circlef=[dot(fy_a,fy_f);dot(fy_b,fy_f);dot(fy_c,fy_f)];
CircleParam=CircleMatrix\Circlef;
a=CircleParam(1)/2;
b=CircleParam(2)/2;

r=(a*a+b*b-CircleParam(3))^(0.5);
po0=PE(1,1:2)-[a,b];
po2=PE(len(1),1:2)-[a,b];
angle=acos(dot(po0,po2)/(r*r));
c=[a,b,r,angle];
end