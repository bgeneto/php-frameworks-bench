<?php

namespace App\Controller;

use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;

class HelloController extends AbstractController
{
    #[Route('/')]
	public function index(): Response
	{
        $version = Symfony\Component\HttpKernel\Kernel::getVersion();
		return $this->render('welcome.html.twig', ['version' => $version]);
	}

    #[Route('/benchmarking/hello')]
    public function hello(): Response
    {
        $data = ['output'=>'Hello, World!!!'];
        return $this->render('benchmarking/hello.html.twig', $data);
    }
}
